import boto3
import zipfile
import argparse
from io import BytesIO

parser = argparse.ArgumentParser()
parser.add_argument('--bucket', '--b', help='Bucket Name')
parser.add_argument('--key', '--k', help='Object Name')
args = parser.parse_args()
print(args)

bucket_name = args.bucket
zip_key = args.key

s3_resource = boto3.resource('s3')
for bucket in s3_resource.buckets.all():
    print(bucket.name)

zip_obj = s3_resource.Object(bucket_name=bucket_name, key=zip_key)
#buffer = BytesIO(zip_obj.get()["Body"].read())
zip = zip_obj.get()["Body"]

#z = zipfile.ZipFile(buffer)
z = zipfile.ZipFile(zip)
for filename in z.namelist():
    file_info = z.getinfo(filename)
    s3_resource.meta.client.upload_fileobj(
        z.open(filename),
        Bucket=bucket,
        Key=f'{filename}'
    )
