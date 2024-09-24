import boto3
import json

def create_bucket(bucket_name):
    s3_client = boto3.client('s3')
    res = s3_client.create_bucket(Bucket=bucket_name)
        
    return res


