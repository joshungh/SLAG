from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
import asyncio
from functools import partial
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DynamoDBService:
    def __init__(self):
        # Ensure AWS credentials are set
        if not os.getenv('AWS_REGION'):
            raise ValueError("AWS_REGION environment variable is not set")
        if not os.getenv('AWS_ACCESS_KEY_ID'):
            raise ValueError("AWS_ACCESS_KEY_ID environment variable is not set")
        if not os.getenv('AWS_SECRET_ACCESS_KEY'):
            raise ValueError("AWS_SECRET_ACCESS_KEY environment variable is not set")

        self.dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.users_table = self.dynamodb.Table('slag_users')

    async def _run_async(self, func, *args, **kwargs):
        """Run a synchronous function asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def create_user(self, user_item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user in DynamoDB."""
        try:
            # Check if username is already taken
            response = await self._run_async(
                self.users_table.scan,
                FilterExpression='username = :username',
                ExpressionAttributeValues={':username': user_item['username']}
            )
            if response['Count'] > 0:
                raise ValueError("Username already taken")

            # Check if wallet address is already registered
            if user_item.get('web3_wallet'):
                response = await self._run_async(
                    self.users_table.scan,
                    FilterExpression='web3_wallet = :wallet',
                    ExpressionAttributeValues={':wallet': user_item['web3_wallet']}
                )
                if response['Count'] > 0:
                    raise ValueError("Wallet address already registered")

            # Set placeholder email for web3 users if email is not provided
            if 'web3' in user_item.get('login_methods', []) and not user_item.get('email'):
                user_item['email'] = f"{user_item['web3_wallet'].lower()}@web3.user"

            # Create the user
            await self._run_async(self.users_table.put_item, Item=user_item)
            return user_item
        except ClientError as e:
            print(f"Error creating user: {e.response['Error']['Message']}")
            raise

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by their ID."""
        try:
            response = await self._run_async(
                self.users_table.get_item,
                Key={
                    'PK': f'USER#{user_id}',
                    'SK': f'USER#{user_id}'
                }
            )
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting user: {e.response['Error']['Message']}")
            raise

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by their email address."""
        try:
            response = await self._run_async(
                self.users_table.scan,
                FilterExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            if response['Count'] > 0:
                return response['Items'][0]
            return None
        except Exception as e:
            raise Exception(f"Error getting user by email: {str(e)}")

    async def get_user_by_wallet(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """Get a user by their wallet address."""
        try:
            response = await self._run_async(
                self.users_table.scan,
                FilterExpression='web3_wallet = :wallet',
                ExpressionAttributeValues={':wallet': wallet_address}
            )
            if response['Count'] > 0:
                return response['Items'][0]
            return None
        except Exception as e:
            raise Exception(f"Error getting user by wallet: {str(e)}")

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
                    expr_values[f":{key}"] = value
            
            # Remove trailing comma and space
            update_expr = update_expr[:-2]
            
            response = await self._run_async(
                self.users_table.update_item,
                Key={
                    'PK': f'USER#{user_id}',
                    'SK': f'USER#{user_id}'
                },
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_values,
                ReturnValues="ALL_NEW"
            )
            return response.get('Attributes')
        except ClientError as e:
            print(f"Error updating user: {e.response['Error']['Message']}")
            raise

    async def update_last_login(self, user_id: str) -> None:
        """Update a user's last login timestamp."""
        try:
            await self._run_async(
                self.users_table.update_item,
                Key={
                    'PK': f'USER#{user_id}',
                    'SK': f'USER#{user_id}'
                },
                UpdateExpression="SET last_login = :now",
                ExpressionAttributeValues={
                    ':now': datetime.utcnow().isoformat()
                }
            )
        except ClientError as e:
            print(f"Error updating last login: {e.response['Error']['Message']}")
            raise 

    async def store_reset_token(self, user_id: str, reset_token: str, expiry: str):
        """Store password reset token in DynamoDB."""
        try:
            await self.users_table.update_item(
                Key={
                    'PK': f'USER#{user_id}',
                    'SK': f'USER#{user_id}'
                },
                UpdateExpression='SET reset_token = :token, reset_token_expiry = :expiry',
                ExpressionAttributeValues={
                    ':token': reset_token,
                    ':expiry': expiry
                }
            )
            return True
        except Exception as e:
            print(f"Error storing reset token: {str(e)}")
            raise e

    async def verify_reset_token(self, token: str) -> bool:
        """Verify if a reset token is valid and not expired."""
        try:
            response = await self.users_table.scan(
                FilterExpression='reset_token = :token',
                ExpressionAttributeValues={
                    ':token': token
                }
            )
            
            if response['Count'] == 0:
                return False
                
            user = response['Items'][0]
            expiry = datetime.fromisoformat(user['reset_token_expiry'])
            
            if datetime.utcnow() > expiry:
                return False
                
            return True
        except Exception as e:
            print(f"Error verifying reset token: {str(e)}")
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
            await self.users_table.update_item(
                Key={
                    'PK': f'USER#{user_id}',
                    'SK': f'USER#{user_id}'
                },
                UpdateExpression='SET password = :password',
                ExpressionAttributeValues={
                    ':password': new_password
                }
            )
            return True
        except Exception as e:
            print(f"Error updating password: {str(e)}")
            raise e

    async def invalidate_reset_token(self, token: str):
        """Remove reset token after password has been reset."""
        try:
            user_id = await self.get_user_id_by_reset_token(token)
            if user_id:
                await self.users_table.update_item(
                    Key={
                        'PK': f'USER#{user_id}',
                        'SK': f'USER#{user_id}'
                    },
                    UpdateExpression='REMOVE reset_token, reset_token_expiry'
                )
            return True
        except Exception as e:
            print(f"Error invalidating reset token: {str(e)}")
            raise e 