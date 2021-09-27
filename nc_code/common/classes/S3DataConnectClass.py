
import pandas as pd
import boto3
import io

from common.utils.decorators import add_attrib

@add_attrib
class S3DataConnect(object):
    """
    class S3DataConnect to create S3 data connection class that can EITHER read or write from/to s3 object,
        using config params, bucket name, file name
    can be used as parent class for more specific S3 reads
    
    """


    def __init__(self, profile_name, bucket, file, **kwargs):

        self.profile_name, self.bucket, self.file = profile_name, bucket, file

        for attrib, value in kwargs.items():
            setattr(self, attrib, value)

        self.s3 = self.gen_s3_client()

    def gen_s3_client(self):

        """
        Method to generate s3 client to use in s3 calls
        """

        session = boto3.Session(profile_name=self.profile_name)
        return session.client('s3')

    def get_s3_obj(self):
        return self.s3.get_object(Bucket=self.bucket,
                                  Key = self.file)

    def write_s3_obj(self):
        return self.s3.upload_file(Filename=self.file,
                                   Bucket=self.bucket,
                                   Key = self.get_attrib('outfile', self.file))


class S3DataReadExcel(S3DataConnect):

    def __init__(self, profile_name, bucket, infile, sheet, **kwargs):

        super().__init__(profile_name, bucket, infile)

        self.s3_response = self.get_s3_obj()

        self.sheet = sheet

        for attrib, value in kwargs.items():
            setattr(self, attrib, value)

        self.df = self.read_excel()


    def read_excel(self):

        excel_file = pd.ExcelFile(io.BytesIO(self.s3_response['Body'].read()))

        df = pd.io.excel.ExcelFile.parse(excel_file, self.sheet, **self.get_attrib('readin_kwargs',{}))

        if hasattr(self, 'renames'):

            df.rename(columns = self.renames, inplace=True)

        return df

