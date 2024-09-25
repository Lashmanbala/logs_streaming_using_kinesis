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