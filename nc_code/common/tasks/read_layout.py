
import pandas as pd
import os

from common.tasks.create_config_class import create_config_class
from common.classes.S3DataConnectClass import S3DataReadExcel

def read_layout(tblname, data_model, **kwargs):
    """
    Function to read in the Excel file database layout from s3 and return df with info for specific table

    params:
        tblname string: name of input table (corresponding excel sheet name)
        data_model string: which data model should be used (raw or datamart)
            options are:
                - 'data_model_rawdata'
                - 'data_model_datamart'
            the value should correspond to the key specified in config to identify the specific data model

        **kwargs: the file name and bucket name that contain the model, will automatically use config to read in unless bucket_name specified -
            if bucket_name is specified in kwargs, will use that instead of config bucket/file path

    returns:
        df with layout sheet for specified tblname
    
    """

    names = ['profile_name','bucket','infile']

    # use exec to convert string name in names list to variable, but must explicitly call from locals() as not updated with exec inside a function! oof!

    if all([name in kwargs.keys() for name in names]):
        for name in names:
            exec(f"{name} = '{kwargs[name]}'")

    else:
        config = create_config_class()

        for name, value in zip(names, [config.DB_PARAMETERS['profile'], config.S3_BUCKETS['data_models'], config.FILES[data_model]]):
            exec(f"{name} = '{value}'")

    kwargs = {'renames' : {'NC Data Element Name' : 'rawcol', 'SQL Name' : 'colname', 'MySQL Type' : 'sqltype'}, \
              'readin_kwargs': {'header' : 4 }}

    s3_read = S3DataReadExcel(locals()['profile_name'], locals()['bucket'], locals()['infile'], tblname, **kwargs)

    return s3_read.df

