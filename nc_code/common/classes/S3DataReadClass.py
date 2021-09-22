
import pandas as pd
import boto3
import io

class S3DataRead(object):
    """
    class S3DataRead to read in s3 object using config params, bucket name, file name -
    can be used as parent class for more specific S3 reads
    
    """


    def __init__(self, profile_name, bucket, infile):

        self.profile_name, self.bucket, self.infile = profile_name, bucket, infile

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