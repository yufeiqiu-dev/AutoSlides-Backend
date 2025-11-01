# app/utils/s3_uploader.py
import boto3
import os
from botocore.config import Config
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from .logger import get_logger

load_dotenv()
logger = get_logger("S3-client")

def create_s3_client():
    """Create and return a configured S3 client with debug logging."""
    try:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_session_token = os.getenv("AWS_SESSION_TOKEN")
        region = os.getenv("AWS_REGION", "us-east-2")
        bucket_name = os.getenv("AWS_BUCKET_NAME")

        # Log basic config (safe info only)
        logger.info("Initializing S3 client...")
        logger.info(f"Region: {region}")
        logger.info(f"Using session token: {'Yes' if aws_session_token else 'No'}")

        # Create the S3 client
        s3_client = boto3.client(
            "s3",
            region_name=region,
            endpoint_url=f"https://s3.{region}.amazonaws.com",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_key,
            aws_session_token=aws_session_token,
            config=Config(signature_version="s3v4")
        )

        # Quick health check
        response = s3_client.list_buckets()
        bucket_names = [b["Name"] for b in response.get("Buckets", [])]
        logger.info(f"Available buckets: {bucket_names}")

        return s3_client, bucket_name

    except NoCredentialsError:
        logger.exception("AWS credentials not found.")
        raise RuntimeError("AWS credentials not found.")
    except Exception as e:
        logger.exception(f"Failed to create S3 client: {e}")
        raise RuntimeError(f"Failed to create S3 client: {e}")

# Instantiate once for global use
s3_client, s3_bucket_name = create_s3_client()

def generate_presigned_url(key, bucket_name=s3_bucket_name, expiration=600):
    try:
        logger.info(f"Generating presigned url for {key} at s3 bucket {bucket_name}")
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": key},
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        logger.error(f"Failed to create presigned URL: {e}")
        raise

def upload_ppt_to_s3(ppt_bytes, user_id, bucket_name=s3_bucket_name):
    try:
        key = f"{user_id}.pptx"
        logger.info(f"Uploading {key} to {bucket_name}")
        s3_client.upload_fileobj(
            ppt_bytes,
            bucket_name,
            key,
            ExtraArgs={"ContentType": "application/vnd.openxmlformats-officedocument.presentationml.presentation"}
        )
        logger.info(f"S3 Upload success for user {user_id}")
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not found")
    except Exception as e:
        raise RuntimeError(f"Failed to upload to S3: {e}")
