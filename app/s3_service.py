import boto3
from io import BytesIO
from config import Config


class S3Service:
    def __init__(self):
        """ Initialises the S3 Service (low-level client and higher-level resource objects) """
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=Config.S3_ACCESS_KEY,
                                      aws_secret_access_key=Config.S3_ACCESS_SECRET_KEY)

        self.s3_resource = boto3.resource('s3',
                                          aws_access_key_id=Config.S3_ACCESS_KEY,
                                          aws_secret_access_key=Config.S3_ACCESS_SECRET_KEY)

    def upload_file(self, bucket_name, s3_key, filename):
        """ Upload a binary file to S3 """
        try:
            with open(filename, "rb") as filedata:
                self.s3_client.upload_fileobj(filedata, bucket_name, s3_key)
        except Exception as e:
            print('Error putting S3 file: {}'.format(e))

    def make_file_public(self, bucket_name, s3_key):
        object_acl = self.s3_resource.ObjectAcl(bucket_name, s3_key)
        object_acl.put(ACL='public-read')

    def upload_binary_data(self, bucket_name, s3_key, bytes_io):
        """ Upload binary data to S3 """
        try:
            self.s3_client.upload_fileobj(bytes_io, bucket_name, s3_key)
        except Exception as e:
            print('Error putting S3 file: {}'.format(e))

    def download_binary_data(self, bucket_name, s3_key):
        """ Download binary data from S3 """
        try:
            bytes_io = BytesIO()
            self.s3_client.download_fileobj(Bucket=bucket_name, Key=s3_key, Fileobj=bytes_io)
            bytes_io.seek(0)
            return bytes_io
        except Exception as e:
            print('Error getting S3 file: {}'.format(e))


