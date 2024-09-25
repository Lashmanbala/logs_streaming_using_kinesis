import boto3
import json
import time

def create_bucket(bucket_name):
    s3_client = boto3.client('s3')
    res = s3_client.create_bucket(Bucket=bucket_name)

    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        bucket_arn = f'arn:aws:s3:::{bucket_name}'
    
    return bucket_arn

def create_iam_role(s3_bucket_name):
    iam_client = boto3.client('iam')

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "firehose.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # Role name
    role_name = 'KinesisFirehoseS3Role'

    # Create the IAM role
    create_role_response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description="Role for Kinesis Firehose to write to S3"
    )

    # Define an inline policy that grants the role S3 write permissions
    s3_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:PutObjectAcl"
                ],
                "Resource": f"arn:aws:s3:::{s3_bucket_name}/*"
            }
        ]
    }

    # Attach the S3 write permissions policy to the role
    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName='KinesisFirehoseS3WritePolicy',
        PolicyDocument=json.dumps(s3_policy)
    )

    arn = create_role_response['Role']['Arn']

    time.sleep(10)  # Wait untill the role is created

    return arn

def create_delivery_stream(delivery_stream_name, s3_bucket_arn, role_arn, S3_path_prefix, buffer_size, buffer_time):
    firehose_client = boto3.client('firehose')

    # Create the delivery stream
    response = firehose_client.create_delivery_stream(
        DeliveryStreamName=delivery_stream_name,
        S3DestinationConfiguration={
            'RoleARN': role_arn,
            'BucketARN': s3_bucket_arn,
            'Prefix': S3_path_prefix,
            'ErrorOutputPrefix': 'error/',
            'BufferingHints': {
                'SizeInMBs': buffer_size,  # Buffer size before data is delivered
                'IntervalInSeconds': buffer_time  # Buffer time before delivery
            },
            'EncryptionConfiguration': {
                'NoEncryptionConfig': 'NoEncryption'  # Use 'NoEncryption' or KMS settings
            },
            'CloudWatchLoggingOptions': {
                'Enabled': True,
                'LogGroupName': 'firehose-delivery-stream-logs',
                'LogStreamName': 'firehose-delivery-stream-log-stream'
            }
        }
    )

    return response