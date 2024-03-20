# `ucimlrepo` package
Package to easily import datasets from the UC Irvine Machine Learning Repository into scripts and notebooks. 
<br>
**Current Version: 0.0.6**

## Installation
In a Jupyter notebook, install with the command 

    !pip3 install -U ucimlrepo 
    
Restart the kernel and import the module `ucimlrepo`.

## Example Usage

    from ucimlrepo import fetch_ucirepo, list_available_datasets
	
	# check which datasets can be imported
	list_available_datasets()
    
    # import dataset
    heart_disease = fetch_ucirepo(id=45)
    # alternatively: fetch_ucirepo(name='Heart Disease')
    
    # access data
    X = heart_disease.data.features
    y = heart_disease.data.targets
    # train model e.g. sklearn.linear_model.LinearRegression().fit(X, y)
    
    # access metadata
    print(heart_disease.metadata.uci_id)
    print(heart_disease.metadata.num_instances)
    print(heart_disease.metadata.additional_info.summary)
    
    # access variable info in tabular format
    print(heart_disease.variables)



## `fetch_ucirepo`
Loads a dataset from the UCI ML Repository, including the dataframes and metadata information.

### Parameters
Provide either a dataset ID or name as keyword (named) arguments. Cannot accept both.
- **`id`**: Dataset ID for UCI ML Repository
- **`name`**: Dataset name, or substring of name

### Returns
- **`dataset`**
	- **`data`**: Contains dataset matrices as **pandas** dataframes
		- `ids`: Dataframe of ID columns
		- `features`: Dataframe of feature columns
		- `targets`: Dataframe of target columns
		- `original`: Dataframe consisting of all IDs, features, and targets
		- `headers`: List of all variable names/headers
	- **`metadata`**: Contains metadata information about the dataset
		- See Metadata section below for details
	- **`variables`**: Contains variable details presented in a tabular/dataframe format
		- `name`: Variable name
		- `role`: Whether the variable is an ID, feature, or target
		- `type`: Data type e.g. categorical, integer, continuous
		- `demographic`: Indicates whether the variable represents demographic data
		- `description`: Short description of variable
		- `units`: variable units for non-categorical data
		- `missing_values`: Whether there are missing values in the variable's column
   

## `list_available_datasets`
Prints a list of datasets that can be imported via `fetch_ucirepo`
### Parameters
- **`filter`**: Optional keyword argument to filter available datasets based on a category
	- Valid filters: `aim-ahead`
- **`search`**: Optional keyword argument to search datasets whose name contains the search query
### Returns
none


## Metadata 
- `uci_id`: Unique dataset identifier for UCI repository 
- `name`
- `abstract`: Short description of dataset
- `area`: Subject area e.g. life science, business
- `task`: Associated machine learning tasks e.g. classification, regression
- `characteristics`: Dataset types e.g. multivariate, sequential
- `num_instances`: Number of rows or samples
- `num_features`: Number of feature columns
- `feature_types`: Data types of features
- `target_col`: Name of target column(s)
- `index_col`: Name of index column(s)
- `has_missing_values`: Whether the dataset contains missing values
- `missing_values_symbol`: Indicates what symbol represents the missing entries (if the dataset has missing values)
- `year_of_dataset_creation`
- `dataset_doi`: DOI registered for dataset that links to UCI repo dataset page
- `creators`: List of dataset creator names
- `intro_paper`: Information about dataset's published introductory paper
- `repository_url`: Link to dataset webpage on the UCI repository
- `data_url`: Link to raw data file
- `additional_info`: Descriptive free text about dataset
	- `summary`: General summary 
	- `purpose`: For what purpose was the dataset created?
	- `funding`: Who funded the creation of the dataset?
	- `instances_represent`: What do the instances in this dataset represent?
	- `recommended_data_splits`: Are there recommended data splits?
	- `sensitive_data`: Does the dataset contain data that might be considered sensitive in any way?
	- `preprocessing_description`: Was there any data preprocessing performed?
	- `variable_info`: Additional free text description for variables
	- `citation`: Citation Requests/Acknowledgements
 - `external_url`: URL to external dataset page. This field will only exist for linked datasets i.e. not hosted by UCI


## Links
- [UCI Machine Learning Repository home page](https://archive.ics.uci.edu/)
- [PyPi repository for this package](https://pypi.org/project/ucimlrepo)
- [Submit an issue](https://github.com/uci-ml-repo/ucimlrepo-feedback/issues)
