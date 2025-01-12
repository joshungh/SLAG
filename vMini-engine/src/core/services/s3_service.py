import boto3
import logging
from datetime import datetime
from pathlib import Path
import os

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = os.getenv('STORY_BUCKET', 'vmini-engine-stories')

    async def save_story(self, content: str, story_id: str, story_type: str = 'story') -> str:
        """Save story content to S3"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            key = f"{story_type}/{story_id}/{timestamp}.md"
            
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=content.encode('utf-8'),
                ContentType='text/markdown'
            )
            
            url = f"s3://{self.bucket}/{key}"
            logger.info(f"Saved {story_type} to S3: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Error saving to S3: {str(e)}")
            raise

    async def get_story(self, story_url: str) -> str:
        """Retrieve story content from S3"""
        try:
            # Parse bucket and key from s3:// URL
            path = Path(story_url.replace('s3://', ''))
            bucket = path.parts[0]
            key = '/'.join(path.parts[1:])
            
            response = self.s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')
            return content
            
        except Exception as e:
            logger.error(f"Error retrieving from S3: {str(e)}")
            raise 