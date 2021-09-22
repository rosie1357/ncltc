
import pandas as pd
import boto3
import io

from common.classes.S3DataReadClass import S3DataRead

class S3DataReadRaw(S3DataRead):
    """
    class S3DataRead to read in data from s3 given specific params (file type, delimters, etc), and
    create df from raw file based on params set in config
    
    """


    def __init__(self, table_name, **kwargs):

        self.table_name = table_name

        # set all config params as attributes

        for attrib, value in kwargs.items():
            setattr(self, attrib, value)

        # initialize with parents args

        super().__init__(self.DB_PARAMETERS['profile'], self.S3_BUCKETS[self.bucket_ref], self.infile)

        self.df = self.read_raw()

    def read_raw(self):
        """
        Method read_raw to read raw data from s3 according to params specified in config and return df to set as self.df
        """

        # read in conditionally based on type, add all readin_kwargs set in config to read_csv()

        if not hasattr(self, 'readin_kwargs'):
            self.readin_kwargs = {}

        if self.file_type == 'csv':
        
            df = pd.read_csv(io.BytesIO(self.s3_response['Body'].read()), engine='python', **self.readin_kwargs)

        if hasattr(self, 'fill_nulls'):
            for col, value in self.fill_nulls.items():
                df[col].fillna(value=value, inplace=True)

        # apply any renames specified in kwargs

        if hasattr(self, 'renames'):

            df.rename(columns = self.renames, inplace=True)

        # all files can have erroneous extra blank lines - drop and return df

        return df.dropna(how='all')
