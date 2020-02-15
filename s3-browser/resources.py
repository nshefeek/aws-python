import boto3
from config import s3_key_id, s3_access_key, bucket
from pprint import pprint

def _get_s3_resource():
    if s3_key_id and s3_access_key:
        return boto3.resource(
            's3',
            aws_access_key_id = s3_key_id,
            aws_secret_access_key = s3_access_key
        )
    else:
        return boto3.resource('s3')

def get_s3_bucket():
    s3_resource = _get_s3_resource()
    return s3_resource.Bucket(bucket)

def get_bucket_list():
    client = boto3.client('s3' )
    return client.list_buckets().get('Buckets')