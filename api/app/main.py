import os
from datetime import datetime
from dotenv import load_dotenv
from core import BambooHRClient, S3Helper
from utils import setup_logger

logger = setup_logger("BambooHR")

# Fetch credentials
load_dotenv()
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
s3_bucket = os.getenv("S3_BUCKET_NAME")
API_KEY = os.getenv("API_KEY")

COMPANY_DOMAIN = "typicode"
ingestion_dt = datetime.now().strftime("%Y-%m-%d")


def main():
    client = BambooHRClient(api_key=API_KEY, company_domain=COMPANY_DOMAIN)
    s3 = S3Helper(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    try:
        logger.info("Fetching data from API...")
        posts = client.get("posts")
        albums = client.get("albums")
        users = client.get("users")
        logger.info("Data successfully pulled from the API")

        logger.info(f"Uploading data to S3 bucket '{s3_bucket}'...")
        s3.upload_json(posts, bucket=s3_bucket, s3_path=f"posts/{ingestion_dt}.json")
        s3.upload_json(albums, bucket=s3_bucket, s3_path=f"albums/{ingestion_dt}.json")
        s3.upload_json(users, bucket=s3_bucket, s3_path=f"users/{ingestion_dt}.json")
        logger.info("Data uploaded to S3")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
