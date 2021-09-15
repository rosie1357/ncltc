
import pandas as pd
import os

from common.tasks.create_config_class import create_config_class

def read_layout(tblname, **kwargs):
    """
    Function to read in the Excel file database layout and return df with info for specific table

    params:
        tblname string: name of input table (corresponding excel sheet name)
        **kwargs: the file path to the layout will be created from below project setup config, but can be overwritten with kwargs:
            if filepath is specified in kwargs, will use that instead of config file path

    returns:
        df with layout sheet for specified tblname
    
    """

    if 'filepath' in kwargs.keys():
        filepath = kwargs['filepath']

    else:
        config = create_config_class()
        filepath = os.path.join(config.PATHS['db_design_dir'], config.FILES['data_model'])

    df = pd.read_excel(filepath, sheet_name=tblname, header=4)

    return df.rename(columns={'NC Data Element Name' : 'rawcol', 'SQL Name' : 'colname', 'MySQL Type' : 'sqltype'})

