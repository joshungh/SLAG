import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

def test_dynamodb_connection():
    try:
        # Initialize DynamoDB client
        dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # Get the users table
        users_table = dynamodb.Table('slag_users')
        
        print("1. Testing table read...")
        # Test reading from table
        response = users_table.scan(Limit=1)
        print(f"✓ Successfully read from table. Found {response['Count']} items")
        
        print("\n2. Testing write operation...")
        # Create a test user item
        test_user_id = str(uuid.uuid4())
        test_item = {
            'PK': f'USER#{test_user_id}',
            'SK': f'USER#{test_user_id}',
            'username': 'test_user',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'created_at': datetime.now().isoformat(),
            'login_methods': ['EMAIL'],
            'author_metadata': {
                'bio': 'Test bio',
                'genres': ['fantasy', 'sci-fi']
            }
        }
        
        users_table.put_item(Item=test_item)
        print(f"✓ Successfully wrote test user with ID: {test_user_id}")
        
        print("\n3. Testing read operation for written item...")
        # Test reading the item we just wrote
        response = users_table.get_item(
            Key={
                'PK': f'USER#{test_user_id}',
                'SK': f'USER#{test_user_id}'
            }
        )
        print("✓ Successfully retrieved test user:")
        print(response['Item'])
        
        print("\n4. Testing delete operation...")
        # Clean up by deleting the test item
        users_table.delete_item(
            Key={
                'PK': f'USER#{test_user_id}',
                'SK': f'USER#{test_user_id}'
            }
        )
        print("✓ Successfully deleted test user")
        
        print("\n✅ All DynamoDB operations completed successfully!")
        
    except ClientError as e:
        print(f"\n❌ Error: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_dynamodb_connection() 