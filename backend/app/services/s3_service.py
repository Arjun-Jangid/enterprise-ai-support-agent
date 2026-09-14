import boto3
from config import S3_BUCKET_NAME


s3_client = boto3.client("s3")


def upload_file_to_s3(local_file_path: str, s3_key: str):
    s3_client.upload_file(
        local_file_path,
        S3_BUCKET_NAME,
        s3_key,
    )