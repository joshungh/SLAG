import boto3
from ...config import settings

def get_bedrock_client():
    """
    Initialize and return AWS Bedrock client
    """
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ) 