import boto3
import json

def create_bucket(bucket_name):
    s3_client = boto3.client('s3')
    res = s3_client.create_bucket(Bucket=bucket_name)
        
    return res

def create_iam_role():
    import boto3

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
    s3_bucket_name = 'your-s3-bucket-name'  # Replace with your actual bucket name
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

    # Print role ARN
    role_arn = create_role_response['Role']['Arn']
    return role_arn
