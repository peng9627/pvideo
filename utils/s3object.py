import os
import sys
import threading

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from pycore.data.entity import config


class S3Object(object):
    def __init__(self, endpoint_url=config.get("s3", "endpoint_url"),
                 aws_access_key_id=config.get("s3", "aws_access_key_id"),
                 aws_secret_access_key=config.get("s3", "aws_secret_access_key"),
                 region_name=config.get("s3", "region_name")):
        self.client = boto3.client('s3', endpoint_url=endpoint_url,
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name=region_name,
                                   config=Config(signature_version='s3'))

    def upload(self, file_source, bucket, file_path):
        self.client.upload_file(file_source, bucket, file_path, ExtraArgs={'ACL': 'public-read'},
                                Callback=UploadProgressPercentage(file_source))

    def delete(self, bucket, file_path):
        s = self.client.delete_object(Bucket=bucket, Key=file_path)
        print s

    def exist(self, bucket, file_path):
        try:
            self.client.head_object(Bucket=bucket, Key=file_path)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True


class UploadProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
