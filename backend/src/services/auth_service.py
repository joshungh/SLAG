import jwt
import bcrypt
from datetime import datetime, timedelta
import uuid
from typing import Optional, Dict, Any
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from .dynamodb_service import DynamoDBService
from ..models.user import UserCreate, UserLogin, LoginMethod
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.db = DynamoDBService()
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
        self.google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.token_expiry = int(os.getenv('TOKEN_EXPIRY_HOURS', '24'))

    def _generate_token(self, user_id: str, login_method: str) -> str:
        """Generate JWT token for authenticated user."""
        payload = {
            'user_id': user_id,
            'login_method': login_method,
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hashed password."""
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    async def register_email_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user with email or web3."""
        # Validate based on login method
        if user_data.login_method == LoginMethod.EMAIL:
            if not user_data.email or not user_data.password:
                raise ValueError("Email and password are required for email registration")
            # Check if email already exists
            existing_user = await self.db.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError("Email already registered")
        elif user_data.login_method == LoginMethod.WEB3:
            if not user_data.web3_wallet:
                raise ValueError("Wallet address is required for web3 registration")
            # Check if wallet already exists
            existing_user = await self.db.get_user_by_wallet(user_data.web3_wallet)
            if existing_user:
                raise ValueError("Wallet address already registered")

        # Create user data
        user_id = str(uuid.uuid4())
        user_dict = {
            'PK': f'USER#{user_id}',
            'SK': f'USER#{user_id}',
            'username': user_data.username,
            'email': user_data.email if user_data.login_method == LoginMethod.EMAIL else f"{user_data.web3_wallet.lower()}@web3.user",
            'password': self._hash_password(user_data.password) if user_data.login_method == LoginMethod.EMAIL else None,
            'web3_wallet': user_data.web3_wallet,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'login_methods': [user_data.login_method.value],
            'created_at': datetime.utcnow().isoformat()
        }

        # Save to database
        created_user = await self.db.create_user(user_dict)
        token = self._generate_token(user_id, user_data.login_method.value)

        return {
            'user': {k: v for k, v in created_user.items() if k != 'password'},
            'token': token
        }

    async def login_email_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Login user with email and password."""
        if not login_data.email or not login_data.password:
            raise ValueError("Email and password are required")

        user = await self.db.get_user_by_email(login_data.email)
        if not user or not self._verify_password(login_data.password, user.get('password', '')):
            raise ValueError("Invalid email or password")

        user_id = user['PK'].split('#')[1]  # Extract user_id from PK
        # Update last login
        await self.db.update_last_login(user_id)
        token = self._generate_token(user_id, LoginMethod.EMAIL.value)

        return {
            'user': {k: v for k, v in user.items() if k != 'password'},
            'token': token
        }

    async def verify_google_token(self, token: str) -> Dict[str, Any]:
        """Verify Google OAuth token and get user info."""
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.google_client_id)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid issuer')

            return {
                'email': idinfo['email'],
                'username': idinfo.get('name', '').replace(' ', '_').lower(),
                'first_name': idinfo.get('given_name'),
                'last_name': idinfo.get('family_name'),
                'profile_picture': idinfo.get('picture')
            }
        except Exception as e:
            raise ValueError(f"Invalid Google token: {str(e)}")

    async def login_google_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Login or register user with Google OAuth."""
        if not login_data.google_token:
            raise ValueError("Google token is required")

        # Verify Google token
        google_user = await self.verify_google_token(login_data.google_token)
        
        # Check if user exists
        user = await self.db.get_user_by_email(google_user['email'])
        
        if not user:
            # Create new user
            user_id = str(uuid.uuid4())
            user_dict = {
                'PK': f'USER#{user_id}',
                'SK': f'USER#{user_id}',
                'username': google_user['username'],
                'email': google_user['email'],
                'first_name': google_user['first_name'],
                'last_name': google_user['last_name'],
                'profile_picture': google_user['profile_picture'],
                'login_methods': [LoginMethod.GOOGLE.value],
                'created_at': datetime.utcnow().isoformat()
            }
            user = await self.db.create_user(user_dict)
        else:
            # Update login methods if needed
            user_id = user['PK'].split('#')[1]
            if LoginMethod.GOOGLE.value not in user.get('login_methods', []):
                login_methods = user.get('login_methods', []) + [LoginMethod.GOOGLE.value]
                await self.db.update_user(user_id, {'login_methods': login_methods})

        # Update last login
        await self.db.update_last_login(user_id)
        token = self._generate_token(user_id, LoginMethod.GOOGLE.value)

        return {
            'user': user,
            'token': token
        }

    async def login_web3_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Login or register user with Web3 wallet."""
        if not login_data.web3_wallet:
            raise ValueError("Web3 wallet address is required")

        # Check if user exists
        user = await self.db.get_user_by_wallet(login_data.web3_wallet)
        
        if not user:
            # Create new user
            user_id = str(uuid.uuid4())
            username = f"user_{user_id[:8]}"
            user_dict = {
                'PK': f'USER#{user_id}',
                'SK': f'USER#{user_id}',
                'username': username,
                'web3_wallet': login_data.web3_wallet,
                'login_methods': [LoginMethod.WEB3.value],
                'created_at': datetime.utcnow().isoformat()
            }
            user = await self.db.create_user(user_dict)
        else:
            user_id = user['PK'].split('#')[1]
        
        # Update last login
        await self.db.update_last_login(user_id)
        token = self._generate_token(user_id, LoginMethod.WEB3.value)

        return {
            'user': user,
            'token': token
        }

    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token and return user data."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            user_id = payload['user_id']
            user = await self.db.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            return {k: v for k, v in user.items() if k != 'password'}
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token") 

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Dict[str, Any]:
        """
        Verify JWT token and return user data.
        This is used as a FastAPI dependency for protected endpoints.
        """
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            if not payload or 'user_id' not in payload:
                raise HTTPException(status_code=401, detail="Invalid token")
                
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e)) 