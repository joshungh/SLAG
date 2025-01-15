import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-west-2')
    )

    # Create Users table
    try:
        users_table = dynamodb.create_table(
            TableName=os.getenv('DYNAMODB_USERS_TABLE', 'slag_users'),
            KeySchema=[
                {
                    'AttributeName': 'PK',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'SK',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'SK',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'web3_wallet',
                    'AttributeType': 'S'  # String
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'email',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'wallet-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'web3_wallet',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Created users table: {users_table['TableDescription']['TableName']}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Users table already exists")

    # Create Stories table
    try:
        stories_table = dynamodb.create_table(
            TableName=os.getenv('DYNAMODB_STORIES_TABLE', 'slag_stories'),
            KeySchema=[
                {
                    'AttributeName': 'PK',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'SK',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'SK',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Created stories table: {stories_table['TableDescription']['TableName']}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Stories table already exists")

if __name__ == "__main__":
    create_tables() 