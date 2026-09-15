import boto3
from config import S3_BUCKET_NAME
from backend.app.core.logging_config import logger


s3_client = boto3.client("s3")


def upload_file_to_s3(local_file_path: str, s3_key: str):
    try:
        logger.info(f"Uploading file to S3: {s3_key}")

        s3_client.upload_file(
            local_file_path,
            S3_BUCKET_NAME,
            s3_key,
        )

        logger.info(f"File uploaded successfully to S3: {s3_key}")

    except Exception:
        logger.exception(f"S3 upload failed: {s3_key}")
        raise