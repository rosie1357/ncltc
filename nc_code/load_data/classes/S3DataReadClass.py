
import pandas as pd
import boto3
import io

class S3DataRead(object):
    """
    class S3DataRead to read in data from s3 given specific params (file type, delimters, etc), and
    create df from raw file based on params set in config
    
    """


    def __init__(self, table_name, **kwargs):
        self.table_name = table_name

        # set all config params as attributes

        for attrib, value in kwargs.items():
            setattr(self, attrib, value)

        self.bucket = self.S3_BUCKETS[self.bucket_ref]

        self.s3 = self.gen_s3_client()
        self.s3_response = self.get_s3_obj()

        self.df = self.read_raw()

    def gen_s3_client(self):

        """
        Method to generate s3 client to use in s3 calls
        """

        session = boto3.Session(profile_name=self.DB_PARAMETERS['profile'])
        return session.client('s3')

    def get_s3_obj(self):
        return self.s3.get_object(Bucket=self.bucket,
                                  Key = self.infile)


    def read_raw(self):
        """
        Method read_raw to read raw data from s3 according to params specified in config and return df to set as self.df
        """

        # read in conditionally based on type

        if self.file_type == 'csv':
            if not hasattr(self, 'delimiter'):
                self.delimiter=','

            if not hasattr(self, 'dtypes'):
                self.dtypes={}

            if not hasattr(self, 'parse_dates'):
                self.parse_dates=[]
        

            df = pd.read_csv(io.BytesIO(self.s3_response['Body'].read()), delimiter = self.delimiter, engine='python', dtype = self.dtypes, parse_dates = self.parse_dates )

        # apply any renames specified in kwargs

        if hasattr(self, 'renames'):

            df.rename(columns = self.renames, inplace=True)

        # all files can have erroneous extra blank lines - drop and return df

        return df.dropna(how='all')
