import json
import urllib.request
from urllib.parse import quote
import pandas as pd
from typing import Optional

from ucimlrepo.dotdict import dotdict

API_BASE_URL = 'https://archive.ics.uci.edu/api/dataset'
DATASET_FILE_BASE_URL = 'https://archive.ics.uci.edu/static/public'


class DatasetNotFoundError(Exception):
    pass

def fetch_ucirepo(
        name: Optional[str] = None, 
        id: Optional[int] = None
    ):

    # check arguments
    # only one or the other
    if name and id:
        raise ValueError('Only specify either dataset name or ID, not both')
    
    # fetch metadata
    api_url = API_BASE_URL
    if name:
        if type(name) != str:
            raise ValueError('Name must be a string')
        api_url += '?name=' + quote(name)
    elif id:
        if type(id) != int:
            raise ValueError('ID must be an integer')
        api_url += '?id=' + str(id)
    else:
        raise ValueError('Must provide a dataset name or ID')


    data = None
    try:
        response  = urllib.request.urlopen(api_url)
        data = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError):
        raise ConnectionError('Error connecting to server')


    # verify that dataset exists 
    if data['status'] != 200:
        list_available_datasets()
        error_msg = data['message'] if 'message' in data else 'Dataset not found in repository'
        raise DatasetNotFoundError(error_msg)
    
    metadata = data['data']
    
    if not id:
        id = metadata['uci_id']
    elif not name:
        name = metadata['name']
    
    # read dataset file
    # url = '{}/{}/data.csv'.format(DATASET_FILE_BASE_URL, id, slug)
    data_url = metadata['data_url']

    if not data_url:
        list_available_datasets()
        raise DatasetNotFoundError('"{}" dataset (id={}) exists in the repository, but is not available for import.'.format(name, id))
    

    df = None
    # parse into dataframe
    try:
        df = pd.read_csv(data_url)
    except (urllib.error.URLError, urllib.error.HTTPError):
        list_available_datasets()
        raise DatasetNotFoundError('Error reading data csv file for "{}" dataset (id={}).'.format(name, id))
        
    if df.empty:
        raise DatasetNotFoundError('Error reading data csv file for "{}" dataset (id={}).'.format(name, id))


    # header line should be attribute names
    headers = df.columns

    # feature information, class labels
    attributes = metadata['attributes']
    del metadata['attributes']
    

    # matrix of features, list of ids, list of targets
    attributes_by_role = {
        'ID': [],
        'Feature': [],
        'Target': []
    }

    for attribute in attributes:
        if attribute['role'] not in attributes_by_role:
            raise ValueError('Role must be one of "ID", "Feature", or "Target"')
        attributes_by_role[attribute['role']].append(attribute['name'])

    # print(attributes_by_role['ID'])
    # print(attributes_by_role['Feature'])
    # print(attributes_by_role['Target'])

    ids_df = df[attributes_by_role['ID']] if len(attributes_by_role['ID']) > 0 else None
    features_df = df[attributes_by_role['Feature']] if len(attributes_by_role['Feature']) > 0 else None
    targets_df = df[attributes_by_role['Target']] if len(attributes_by_role['Target']) > 0 else None


    data = {
        'ids': ids_df,
        'features': features_df,
        'targets': targets_df,
        'original': df,
        'headers': headers,
    }

    attributes = pd.DataFrame.from_records(attributes)

    # alternative usage: 
    # attributes.age.role or attributes.slope.description
    # print(attributes) -> json-like dict with keys [name] -> details

    metadata['additional_info'] = dotdict(metadata['additional_info'])
    metadata['intro_paper'] = dotdict(metadata['intro_paper'])
    
    # construct result object
    result = {
        'data': dotdict(data),
        'metadata': dotdict(metadata),
        'attributes': attributes
    }

    # return
    return dotdict(result)
    


def list_available_datasets():
    print('-------------------------------------')
    print('The following datasets are available:')
    print('-------------------------------------')
    # change to a static/public URL
    with urllib.request.urlopen('{}/info/available_py_datasets.json'.format(DATASET_FILE_BASE_URL)) as resp:
        print('{:<50} {:<6} {:<100}'.format('Dataset Name', 'ID', 'Prediction Task'))
        print('{:<50} {:<6} {:<100}'.format('------------', '--', '---------------'))
        data = json.load(resp)
        for dataset in data:
            print('{:<50} {:<6} {:<100}'.format(dataset['name'], dataset['id'], dataset['description']))
        print()