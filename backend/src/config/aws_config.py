import boto3
import os
from dotenv import load_dotenv

def initialize_aws():
    """Initialize AWS configuration globally"""
    load_dotenv()

    # Set AWS credentials and region in environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
    os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
    os.environ['AWS_DEFAULT_REGION'] = os.getenv('AWS_REGION', 'us-west-2')

    # Configure boto3 globally
    boto3.setup_default_session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-west-2')
    ) 