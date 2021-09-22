
import pandas as pd
import boto3
import io

class S3DataRead(object):
    """
    class S3DataRead to read in s3 object using config params, bucket name, file name -
    can be used as parent class for more specific S3 reads
    
    """


    def __init__(self, profile_name, bucket, infile, **kwargs):

        self.profile_name, self.bucket, self.infile = profile_name, bucket, infile
        print(self.bucket)

        self.s3 = self.gen_s3_client()
        self.s3_response = self.get_s3_obj()

    def gen_s3_client(self):

        """
        Method to generate s3 client to use in s3 calls
        """

        session = boto3.Session(profile_name=self.profile_name)
        return session.client('s3')

    def get_s3_obj(self):
        return self.s3.get_object(Bucket=self.bucket,
                                  Key = self.infile)


class S3DataReadExcel(S3DataRead):

    def __init__(self, profile_name, bucket, infile, sheet, **kwargs):

        super().__init__(profile_name, bucket, infile)

        self.sheet = sheet

        for attrib, value in kwargs.items():
            setattr(self, attrib, value)

        self.df = self.read_excel()


    def read_excel(self):

        excel_file = pd.ExcelFile(io.BytesIO(self.s3_response['Body'].read()))

        if not hasattr(self, 'readin_kwargs'):
            self.readin_kwargs = {}

        df = pd.io.excel.ExcelFile.parse(excel_file, self.sheet, **self.readin_kwargs)

        if hasattr(self, 'renames'):

            df.rename(columns = self.renames, inplace=True)

        return df

