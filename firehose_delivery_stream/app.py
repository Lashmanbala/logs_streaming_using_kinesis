from aws_util import create_bucket, create_iam_role, create_delivery_stream
import dotenv

bucket_name = 'user-logs-bucket-1'
s3_bucket_arn = 'arn:aws:s3:::user-logs-bucket-1' # create_bucket(bucket_name)
print(s3_bucket_arn)

role_arn = create_iam_role(s3_bucket_name = bucket_name)
print(role_arn)

dotenv.load_dotenv()
delivery_stream_name = 'user-logs-s3-stream'
S3_path_prefix = 'logs/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/'
buffer_size = 1
buffer_time = 10
res = create_delivery_stream(delivery_stream_name, s3_bucket_arn, role_arn, S3_path_prefix, buffer_size, buffer_time)
print(res)
 