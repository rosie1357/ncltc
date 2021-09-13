
import pandas as pd
import os

class ReadRawtoLoad(object):
    """
    class ReadRawtoLoad to set all main config params and table-specific params as attributes, and
    create df from raw file based on params set in config
    
    """


    def __init__(self, table_name, **kwargs):
        self.table_name = table_name

        # set all config params as attributes

        for attrib, value in kwargs.items():
            setattr(self, attrib, value)

        self.indir = self.PATHS[self.indir_ref]
        self.df = self.read_raw()


    def read_raw(self):
        """
        Method read_raw to import raw data according to params specified in config and return df to set as self.df
        
        """

        # determine file type from extension

        if self.infile.split('.')[-1] in ['txt','csv']:

            df = pd.read_csv(os.path.join(self.indir,self.infile), delimiter = self.delimiter, dtype = self.dtypes or {})

        return df