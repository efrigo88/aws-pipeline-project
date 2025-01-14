import json
import requests
import boto3

from typing import List
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from botocore.exceptions import BotoCoreError, ClientError
from utils import setup_logger

logger = setup_logger("core_functions")


class BambooHRClient:
    """A client for the BambooHR API.

    This client handles authentication, session management, and API requests
    to the BambooHR API or a placeholder API for demonstration purposes.
    """

    # BASE_URL = "https://api.bamboohr.com/api/gateway.php/{company_domain}/v1"
    BASE_URL = "https://jsonplaceholder.{company_domain}.com"
    ENDPOINTS = {
        "posts": "/posts",
        "albums": "/albums",
        "users": "/users",
    }

    def __init__(self, api_key, company_domain):
        """
        Initialize the BambooHRClient with an API key and company domain.

        Args:
            api_key (str): The API key for authenticating requests.
            company_domain (str): The domain of the company for API requests.
        """
        self.api_key = api_key
        self.company_domain = company_domain
        self.base_url = self.BASE_URL.format(company_domain=company_domain)
        self.session = self._create_session()
        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "Accept": "application/json",
        }

    def _create_session(self) -> requests.Session:
        """Create a session with a retry strategy for handling transient errors."""
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[429, 503],
            allowed_methods=["GET"],
        )

        # Create an adapter with the retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)

        # Create a session and mount the adapter
        session = requests.Session()
        session.mount("https://", adapter)

        return session

    def get(self, endpoint_key: str, params: dict = None) -> dict:
        """
        Fetch data from a specified endpoint using the endpoint key.

        Args:
            endpoint_key (str): The key for the desired endpoint (e.g., "posts").
            params (dict, optional): Query parameters to include in the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ValueError: If an invalid endpoint key is provided.
            requests.exceptions.RequestException: If the request fails.

        Example:
            >>> client = BambooHRClient(api_key="my_api_key", company_domain="typicode")
            >>> posts = client.get("posts")
            >>> print(posts)
        """
        endpoint = self.ENDPOINTS.get(endpoint_key)
        if not endpoint:
            raise ValueError(f"Invalid endpoint key: {endpoint_key}")
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()


class S3Helper:
    """Utility class for handling S3 operations."""

    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str = "eu-east-1",
    ):
        """
        Initializes the S3Helper with AWS credentials and region.

        Args:
            aws_access_key_id (str): Your AWS access key ID.
            aws_secret_access_key (str): Your AWS secret access key.
            region_name (str): The AWS region to connect to (default: "us-east-1").
        """
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def upload_json(self, data: List[dict], s3_path: str, bucket: str):
        """
        Upload JSON data to an S3 bucket.

        Args:
            data (List[dict]): The data to upload.
            s3_path (str): The S3 key/path where the file will be saved.
            bucket (str): The S3 bucket name.
        """
        try:
            json_data = json.dumps(data)
            self.s3_client.put_object(Bucket=bucket, Key=s3_path, Body=json_data)
            logger.info(f"Data uploaded to s3://{bucket}/{s3_path}")
        except (BotoCoreError, ClientError) as e:
            logger.error("Failed to upload data to S3.", e)
            raise
