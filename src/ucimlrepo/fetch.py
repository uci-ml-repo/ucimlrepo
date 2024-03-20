import json
import pandas as pd
from typing import Optional
import urllib.request
import urllib.parse
import certifi
import ssl

from ucimlrepo.dotdict import dotdict


# constants

# API endpoints
API_BASE_URL = 'https://archive.ics.uci.edu/api/dataset'
API_LIST_URL = 'https://archive.ics.uci.edu/api/datasets/list'

# base location of data csv files
DATASET_FILE_BASE_URL = 'https://archive.ics.uci.edu/static/public'

# available categories of datasets to filter by 
VALID_FILTERS = ['aim-ahead']


# custom exception for no dataset found during fetch_ucirepo
class DatasetNotFoundError(Exception):
    pass


def fetch_ucirepo(
        name: Optional[str] = None, 
        id: Optional[int] = None
    ):
    '''
    Loads a dataset from the UCI ML Repository, including the dataframes and metadata information.

    Parameters: 
        id (int): Dataset ID for UCI ML Repository
        name (str): Dataset name, or substring of name
        (Only provide id or name, not both)

    Returns:
        result (dotdict): object containing dataset metadata, dataframes, and variable info in its properties
    '''

    # check that only one argument is provided
    if name and id:
        raise ValueError('Only specify either dataset name or ID, not both')
    
    # validate types of arguments and add them to the endpoint query string
    api_url = API_BASE_URL
    if name:
        if type(name) != str:
            raise ValueError('Name must be a string')
        api_url += '?name=' + urllib.parse.quote(name)
    elif id:
        if type(id) != int:
            raise ValueError('ID must be an integer')
        api_url += '?id=' + str(id)
    else:
        # no arguments provided
        raise ValueError('Must provide a dataset name or ID')


    # fetch metadata from API
    data = None
    try:
        response = urllib.request.urlopen(api_url, context=ssl.create_default_context(cafile=certifi.where()))
        data = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError):
        raise ConnectionError('Error connecting to server')

    # verify that dataset exists 
    if data['status'] != 200:
        error_msg = data['message'] if 'message' in data else 'Dataset not found in repository'
        raise DatasetNotFoundError(error_msg)
    

    # extract ID, name, and URL from metadata
    metadata = data['data']
    if not id:
        id = metadata['uci_id']
    elif not name:
        name = metadata['name']
    
    data_url = metadata['data_url']

    # no data URL means that the dataset cannot be imported into Python
    # i.e. it does not yet have a standardized CSV file for pandas to parse
    if not data_url:
        raise DatasetNotFoundError('"{}" dataset (id={}) exists in the repository, but is not available for import. Please select a dataset from this list: https://archive.ics.uci.edu/datasets?skip=0&take=10&sort=desc&orderBy=NumHits&search=&Python=true'.format(name, id))
    

    # parse into dataframe using pandas
    df = None
    try:
        df = pd.read_csv(data_url)
    except (urllib.error.URLError, urllib.error.HTTPError):
        raise DatasetNotFoundError('Error reading data csv file for "{}" dataset (id={}).'.format(name, id))
        
    if df.empty:
        raise DatasetNotFoundError('Error reading data csv file for "{}" dataset (id={}).'.format(name, id))


    # header line should be variable names
    headers = df.columns

    # feature information, class labels
    variables = metadata['variables']
    del metadata['variables']      # moved from metadata to a separate property
    
    # organize variables into IDs, features, or targets
    variables_by_role = {
        'ID': [],
        'Feature': [],
        'Target': [],
        'Other': []
    }
    for variable in variables:
        if variable['role'] not in variables_by_role:
            raise ValueError('Role must be one of "ID", "Feature", or "Target", or "Other"')
        variables_by_role[variable['role']].append(variable['name'])

    # extract dataframes for each variable role
    ids_df = df[variables_by_role['ID']] if len(variables_by_role['ID']) > 0 else None
    features_df = df[variables_by_role['Feature']] if len(variables_by_role['Feature']) > 0 else None
    targets_df = df[variables_by_role['Target']] if len(variables_by_role['Target']) > 0 else None

    # place all varieties of dataframes in data object
    data = {
        'ids': ids_df,
        'features': features_df,
        'targets': targets_df,
        'original': df,
        'headers': headers,
    }

    # convert variables from JSON structure to tabular structure for easier visualization
    variables = pd.DataFrame.from_records(variables)

    # alternative usage?: 
    # variables.age.role or variables.slope.description
    # print(variables) -> json-like dict with keys [name] -> details

    # make nested metadata fields accessible via dot notation
    metadata['additional_info'] = dotdict(metadata['additional_info']) if metadata['additional_info'] else None
    metadata['intro_paper'] = dotdict(metadata['intro_paper']) if metadata['intro_paper'] else None
    
    # construct result object
    result = {
        'data': dotdict(data),
        'metadata': dotdict(metadata),
        'variables': variables
    }

    # convert to dictionary with dot notation
    return dotdict(result)
    


def list_available_datasets(filter: Optional[str] = None, search: Optional[str] = None, area: Optional[str] = None):
    '''
    Prints a list of datasets that can be imported via fetch_ucirepo function

    Parameters: 
        filter (str): Optional query to filter available datasets based on a label
        search (str): Optional query to search for available datasets by name
        area (str): Optional query to filter available datasets based on subject area

    Returns:
        None
    '''

    # validate filter input
    if filter:
        if type(filter) != str:
            raise ValueError('Filter must be a string') 
        filter = filter.lower()
        
    # validate search input
    if search:
        if type(search) != str:
            raise ValueError('Search query must be a string')
        search = search.lower()
    
    # construct endpoint URL
    api_list_url = API_LIST_URL
    query_params = {}
    if filter:
        query_params['filter'] = filter
    else: 
        query_params['filter'] = 'python'       # default filter should be 'python'
    if search:
        query_params['search'] = search
    if area:
        query_params['area'] = area

    api_list_url += '?' + urllib.parse.urlencode(query_params)

    # fetch list of datasets from API
    data = None
    try:
        response  = urllib.request.urlopen(api_list_url, context=ssl.create_default_context(cafile=certifi.where()))
        resp_json = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError):
        raise ConnectionError('Error connecting to server')

    if resp_json['status'] != 200:
        error_msg = resp_json['message'] if 'message' in resp_json else 'Internal Server Error'
        raise ValueError(resp_json['message'])
    
    data = resp_json['data']

    if len(data) == 0:
        print('No datasets found')
        return
    
    # column width for dataset name
    maxNameLen = max(max([len(dataset['name']) for dataset in data]) + 3, 15)

    # print table title
    title = 'The following {}datasets are available{}:'.format(filter + ' ' if filter else '', ' for search query "{}"'.format(search) if search else '')
    print('-' * len(title))
    print(title)
    print('-' * len(title))

    # print table headers
    header_str = '{:<{width}} {:<6}'.format('Dataset Name', 'ID', width=maxNameLen)
    underline_str = '{:<{width}} {:<6}'.format('------------', '--', width=maxNameLen)
    if len(data) > 0 and 'description' in data[0]:
        header_str += ' {:<100}'.format('Prediction Task')
        underline_str += ' {:<100}'.format('---------------')
    print(header_str)
    print(underline_str)
    
    # print row for each dataset
    for dataset in data:
        row_str = '{:<{width}} {:<6}'.format(dataset['name'], dataset['id'], width=maxNameLen)
        if 'description' in dataset:
            row_str += ' {:<100}'.format(dataset['description'])
        print(row_str)
    
    print()
