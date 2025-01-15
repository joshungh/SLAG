from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
import asyncio
from functools import partial
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DynamoDBService:
    def __init__(self):
        try:
            # Initialize the DynamoDB client with explicit credentials
            self.dynamodb = boto3.client('dynamodb',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-west-2')
            )
            
            # Test the connection
            self.dynamodb.list_tables()
            
            self.users_table = os.getenv('DYNAMODB_USERS_TABLE', 'slag_users')
            self.stories_table = os.getenv('DYNAMODB_STORIES_TABLE', 'slag_stories')
            logger.info("Successfully initialized DynamoDB connection")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"Failed to initialize DynamoDB connection. Error: {error_code} - {error_message}")
            logger.error(f"AWS Region: {os.getenv('AWS_REGION')}")
            logger.error(f"Access Key ID: {os.getenv('AWS_ACCESS_KEY_ID')[:5]}...")  # Log only first 5 chars for security
            raise

    async def _run_async(self, func, *args, **kwargs):
        """Run a synchronous function asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def create_user(self, user_item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user in DynamoDB."""
        try:
            # Check if username is already taken
            response = await self._run_async(
                self.dynamodb.scan,
                TableName=self.users_table,
                FilterExpression='username = :username',
                ExpressionAttributeValues={
                    ':username': {'S': user_item['username']}
                }
            )
            if response.get('Count', 0) > 0:
                raise ValueError("Username already taken")

            # Check if wallet address is already registered
            if user_item.get('web3_wallet'):
                response = await self._run_async(
                    self.dynamodb.scan,
                    TableName=self.users_table,
                    FilterExpression='web3_wallet = :wallet',
                    ExpressionAttributeValues={
                        ':wallet': {'S': user_item['web3_wallet']}
                    }
                )
                if response.get('Count', 0) > 0:
                    raise ValueError("Wallet address already registered")

            # Set placeholder email for web3 users if email is not provided
            if 'web3' in user_item.get('login_methods', []) and not user_item.get('email'):
                user_item['email'] = f"{user_item['web3_wallet'].lower()}@web3.user"

            # Convert the user_item to DynamoDB format
            dynamodb_item = {}
            for key, value in user_item.items():
                if isinstance(value, str):
                    dynamodb_item[key] = {'S': value}
                elif isinstance(value, bool):
                    dynamodb_item[key] = {'BOOL': value}
                elif isinstance(value, (int, float)):
                    dynamodb_item[key] = {'N': str(value)}
                elif isinstance(value, list):
                    dynamodb_item[key] = {'SS': value} if all(isinstance(x, str) for x in value) else {'L': [{'S': str(x)} for x in value]}
                elif value is None:
                    continue
                else:
                    dynamodb_item[key] = {'S': str(value)}

            # Create the user
            await self._run_async(
                self.dynamodb.put_item,
                TableName=self.users_table,
                Item=dynamodb_item
            )
            return user_item
        except ClientError as e:
            logger.error(f"Error creating user: {e.response['Error']['Message']}")
            raise

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by their ID."""
        try:
            response = await self._run_async(
                self.dynamodb.get_item,
                TableName=self.users_table,
                Key={
                    'PK': {'S': f'USER#{user_id}'},
                    'SK': {'S': f'USER#{user_id}'}
                }
            )
            item = response.get('Item')
            return self._deserialize_item(item) if item else None
        except ClientError as e:
            logger.error(f"Error getting user: {e.response['Error']['Message']}")
            raise

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by their email address."""
        try:
            response = await self._run_async(
                self.dynamodb.scan,
                TableName=self.users_table,
                FilterExpression='email = :email',
                ExpressionAttributeValues={
                    ':email': {'S': email}
                }
            )
            items = response.get('Items', [])
            if items:
                return self._deserialize_item(items[0])
            return None
        except ClientError as e:
            logger.error(f"Error getting user by email: {e.response['Error']['Message']}")
            raise

    async def get_user_by_wallet(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """Get user by wallet address."""
        try:
            response = await self._run_async(
                self.dynamodb.scan,
                TableName=self.users_table,
                FilterExpression='web3_wallet = :wallet',
                ExpressionAttributeValues={
                    ':wallet': {'S': wallet_address}
                }
            )
            items = response.get('Items', [])
            if items:
                return self._deserialize_item(items[0])
            return None
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"Error querying user by wallet. Error: {error_code} - {error_message}")
            logger.error(f"Wallet address: {wallet_address}")
            raise

    def _deserialize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Convert DynamoDB item to Python dict."""
        if not item:
            return {}
        
        result = {}
        for key, value in item.items():
            # Get the first key in the value dict (e.g., 'S', 'N', etc.)
            type_key = next(iter(value))
            # Handle special cases for certain fields
            if key == 'password':
                # Ensure password is always returned as a UTF-8 string
                if not value[type_key]:
                    result[key] = None
                else:
                    try:
                        result[key] = str(value[type_key])
                    except Exception as e:
                        logger.error(f"Error deserializing password: {str(e)}")
                        result[key] = None
            elif type_key == 'N':
                # Convert numbers to float or int
                num_val = value[type_key]
                result[key] = int(num_val) if num_val.isdigit() else float(num_val)
            elif type_key == 'BOOL':
                # Convert to boolean
                result[key] = value[type_key]
            elif type_key == 'NULL':
                # Handle null values
                result[key] = None
            elif type_key == 'L':
                # Handle lists
                result[key] = [self._deserialize_value(v) for v in value[type_key]]
            elif type_key == 'M':
                # Handle maps
                result[key] = {k: self._deserialize_value(v) for k, v in value[type_key].items()}
            else:
                # Default case for strings and other types
                result[key] = value[type_key]
        return result

    def _deserialize_value(self, value: Dict[str, Any]) -> Any:
        """Helper method to deserialize a single DynamoDB value."""
        type_key = next(iter(value))
        if type_key == 'N':
            num_val = value[type_key]
            return int(num_val) if num_val.isdigit() else float(num_val)
        elif type_key == 'BOOL':
            return value[type_key]
        elif type_key == 'NULL':
            return None
        elif type_key == 'L':
            return [self._deserialize_value(v) for v in value[type_key]]
        elif type_key == 'M':
            return {k: self._deserialize_value(v) for k, v in value[type_key].items()}
        else:
            return value[type_key]

    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a user's information."""
        try:
            # Build update expression
            update_expr = "SET "
            expr_names = {}
            expr_values = {}
            
            for key, value in update_data.items():
                if value is not None:  # Only update non-null values
                    update_expr += f"#{key} = :{key}, "
                    expr_names[f"#{key}"] = key
                    # Convert value to DynamoDB format
                    if isinstance(value, str):
                        expr_values[f":{key}"] = {'S': value}
                    elif isinstance(value, bool):
                        expr_values[f":{key}"] = {'BOOL': value}
                    elif isinstance(value, (int, float)):
                        expr_values[f":{key}"] = {'N': str(value)}
                    elif isinstance(value, list):
                        expr_values[f":{key}"] = {'SS': value} if all(isinstance(x, str) for x in value) else {'L': [{'S': str(x)} for x in value]}
                    else:
                        expr_values[f":{key}"] = {'S': str(value)}

            # Remove trailing comma and space
            update_expr = update_expr[:-2]

            response = await self._run_async(
                self.dynamodb.update_item,
                TableName=self.users_table,
                Key={
                    'PK': {'S': f'USER#{user_id}'},
                    'SK': {'S': f'USER#{user_id}'}
                },
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_values,
                ReturnValues="ALL_NEW"
            )
            return self._deserialize_item(response.get('Attributes', {}))
        except ClientError as e:
            logger.error(f"Error updating user: {e.response['Error']['Message']}")
            raise

    async def update_last_login(self, user_id: str) -> None:
        """Update a user's last login timestamp."""
        try:
            await self._run_async(
                self.dynamodb.update_item,
                TableName=self.users_table,
                Key={
                    'PK': {'S': f'USER#{user_id}'},
                    'SK': {'S': f'USER#{user_id}'}
                },
                UpdateExpression="SET last_login = :now",
                ExpressionAttributeValues={
                    ':now': {'S': datetime.utcnow().isoformat()}
                }
            )
        except ClientError as e:
            logger.error(f"Error updating last login: {e.response['Error']['Message']}")
            raise

    async def store_reset_token(self, user_id: str, reset_token: str, expiry: str):
        """Store password reset token in DynamoDB."""
        try:
            await self._run_async(
                self.dynamodb.update_item,
                TableName=self.users_table,
                Key={
                    'PK': {'S': f'USER#{user_id}'},
                    'SK': {'S': f'USER#{user_id}'}
                },
                UpdateExpression='SET reset_token = :token, reset_token_expiry = :expiry',
                ExpressionAttributeValues={
                    ':token': {'S': reset_token},
                    ':expiry': {'S': expiry}
                }
            )
            return True
        except ClientError as e:
            logger.error(f"Error storing reset token: {e.response['Error']['Message']}")
            raise

    async def verify_reset_token(self, token: str) -> bool:
        """Verify if a reset token is valid and not expired."""
        try:
            response = await self._run_async(
                self.dynamodb.scan,
                TableName=self.users_table,
                FilterExpression='reset_token = :token',
                ExpressionAttributeValues={
                    ':token': {'S': token}
                }
            )

            if response.get('Count', 0) == 0:
                return False

            items = response.get('Items', [])
            if not items:
                return False

            user = self._deserialize_item(items[0])
            expiry = datetime.fromisoformat(user['reset_token_expiry'])

            if datetime.utcnow() > expiry:
                return False

            return True
        except ClientError as e:
            logger.error(f"Error verifying reset token: {e.response['Error']['Message']}")
            return False

    async def get_user_id_by_reset_token(self, token: str) -> Optional[str]:
        """Get user ID associated with a reset token."""
        try:
            response = await self.users_table.scan(
                FilterExpression='reset_token = :token',
                ExpressionAttributeValues={
                    ':token': token
                }
            )

            if response['Count'] == 0:
                return None

            user = response['Items'][0]
            return user['PK'].split('#')[1]
        except Exception as e:
            print(f"Error getting user by reset token: {str(e)}")
            return None

    async def update_password(self, user_id: str, new_password: str):
        """Update user's password."""
        try:
            await self._run_async(
                self.dynamodb.update_item,
                TableName=self.users_table,
                Key={
                    'PK': {'S': f'USER#{user_id}'},
                    'SK': {'S': f'USER#{user_id}'}
                },
                UpdateExpression='SET password = :password',
                ExpressionAttributeValues={
                    ':password': {'S': new_password}
                }
            )
            return True
        except ClientError as e:
            logger.error(f"Error updating password: {e.response['Error']['Message']}")
            raise

    async def invalidate_reset_token(self, token: str):
        """Remove reset token after password has been reset."""
        try:
            user_id = await self.get_user_id_by_reset_token(token)
            if user_id:
                await self._run_async(
                    self.dynamodb.update_item,
                    TableName=self.users_table,
                    Key={
                        'PK': {'S': f'USER#{user_id}'},
                        'SK': {'S': f'USER#{user_id}'}
                    },
                    UpdateExpression='REMOVE reset_token, reset_token_expiry'
                )
            return True
        except ClientError as e:
            logger.error(f"Error invalidating reset token: {e.response['Error']['Message']}")
            raise

    async def create_story(self, story_item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new story in DynamoDB."""
        try:
            # Convert the story_item to DynamoDB format
            dynamodb_item = {}
            for key, value in story_item.items():
                if isinstance(value, str):
                    dynamodb_item[key] = {'S': value}
                elif isinstance(value, bool):
                    dynamodb_item[key] = {'BOOL': value}
                elif isinstance(value, (int, float)):
                    dynamodb_item[key] = {'N': str(value)}
                elif isinstance(value, list):
                    dynamodb_item[key] = {'SS': value} if all(isinstance(x, str) for x in value) else {'L': [{'S': str(x)} for x in value]}
                elif value is None:
                    continue
                else:
                    dynamodb_item[key] = {'S': str(value)}

            # Create the story
            await self._run_async(
                self.dynamodb.put_item,
                TableName=self.stories_table,
                Item=dynamodb_item
            )
            return story_item
        except ClientError as e:
            logger.error(f"Error creating story: {e.response['Error']['Message']}")
            raise

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a user by their username."""
        try:
            response = await self._run_async(
                self.dynamodb.scan,
                TableName=self.users_table,
                FilterExpression='username = :username',
                ExpressionAttributeValues={
                    ':username': {'S': username}
                }
            )
            items = response.get('Items', [])
            if items:
                return self._deserialize_item(items[0])
            return None
        except ClientError as e:
            logger.error(f"Error getting user by username: {e.response['Error']['Message']}")
            raise
