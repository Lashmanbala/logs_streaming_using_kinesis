from aws_util import create_bucket, create_iam_role

bkt_name = 'user-logs-bucket-1'
def return_bucket_arn(bkt_name):
    bucket_res = create_bucket(bkt_name)
    if bucket_res['ResponseMetadata']['HTTPStatusCode'] == 200:
        bucket_arn = f'arn:aws:s3:::{bkt_name}'
        return bucket_arn

arn = return_bucket_arn(bkt_name)
print(arn)

role_arn = create_iam_role()
print(role_arn)