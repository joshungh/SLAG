from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import uuid
from datetime import datetime, timedelta
import bcrypt
import secrets
from ..services.dynamodb_service import DynamoDBService
from ..services.auth_service import AuthService
from ..models.user import UserCreate, LoginMethod, UserLogin
from ..services.email_service import EmailService

router = APIRouter()
db = DynamoDBService()
auth_service = AuthService()
email_service = EmailService()

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed password."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

@router.post("/auth/login")
async def login(user_login: UserLogin):
    """Login user and return JWT token."""
    try:
        # Handle email login
        if user_login.login_method == LoginMethod.EMAIL:
            if not user_login.email or not user_login.password:
                raise ValueError("Email and password are required for email login")
            
            # Get user by email
            user = await db.get_user_by_email(user_login.email)
            if not user:
                raise ValueError("Invalid email or password")
            
            # Verify password
            if not verify_password(user_login.password, user['password']):
                raise ValueError("Invalid email or password")
            
            # Generate JWT token
            token = auth_service._generate_token(user['PK'].split('#')[1], user_login.login_method.value)
            
            # Remove password from response
            if 'password' in user:
                del user['password']
            
            return {
                "user": user,
                "token": token
            }
            
        # Handle web3 login
        elif user_login.login_method == LoginMethod.WEB3:
            if not user_login.web3_wallet:
                raise ValueError("Wallet address is required for web3 login")
            
            user = await db.get_user_by_wallet(user_login.web3_wallet)
            if not user:
                raise ValueError("User not found")
            
            # Generate JWT token
            token = auth_service._generate_token(user['PK'].split('#')[1], user_login.login_method.value)
            
            return {
                "user": user,
                "token": token
            }
            
        else:
            raise ValueError("Unsupported login method")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

@router.get("/auth/verify")
async def verify_token(token: str = Depends(auth_service.get_current_user)):
    """Verify JWT token and return user data."""
    try:
        # Get user ID from token
        user_id = token.get("user_id")
        if not user_id:
            raise ValueError("Invalid token")
            
        # Get user data
        user = await db.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
            
        # Remove password from response
        if 'password' in user:
            del user['password']
            
        return {
            "user": user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/users")
async def create_user(user: UserCreate):
    """Create a new user."""
    try:
        # Generate a unique user ID
        user_id = str(uuid.uuid4())
        
        # Create user item for DynamoDB
        user_item = {
            'PK': f'USER#{user_id}',
            'SK': f'USER#{user_id}',
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'web3_wallet': user.web3_wallet,
            'login_methods': [user.login_method],
            'created_at': datetime.utcnow().isoformat(),
            'author_metadata': {
                'bio': '',
                'genres': []
            }
        }

        # Hash password for email registration
        if user.login_method == LoginMethod.EMAIL:
            if not user.password:
                raise ValueError("Password is required for email registration")
            user_item['password'] = hash_password(user.password)
        
        # Save to DynamoDB
        created_user = await db.create_user(user_item)
        # Remove password from response
        if 'password' in created_user:
            del created_user['password']

        # Generate JWT token
        token = auth_service._generate_token(user_id, user.login_method.value)
            
        return {
            "user": created_user,
            "token": token
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/users/wallet/{wallet_address}")
async def get_user_by_wallet(wallet_address: str):
    """Get user by wallet address."""
    try:
        user = await db.get_user_by_wallet(wallet_address)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user by ID."""
    try:
        user = await db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")

@router.put("/users/{user_id}")
async def update_user(user_id: str, user_update: UserCreate):
    """Update user information."""
    try:
        # Create update item for DynamoDB
        update_item = {
            'username': user_update.username,
            'email': user_update.email,
            'first_name': user_update.first_name,
            'last_name': user_update.last_name,
            'web3_wallet': user_update.web3_wallet,
            'login_methods': user_update.login_methods,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Update in DynamoDB
        updated_user = await db.update_user(user_id, update_item)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}") 

@router.post("/auth/forgot-password")
async def request_password_reset(email: str):
    """Request a password reset token."""
    try:
        user = await db.get_user_by_email(email)
        if not user:
            # Return success even if user not found to prevent email enumeration
            return {"message": "If an account exists with this email, a password reset link has been sent."}
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        reset_token_expiry = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        
        # Store reset token in DynamoDB
        await db.store_reset_token(user['PK'].split('#')[1], reset_token, reset_token_expiry)
        
        # Send reset email
        reset_url = f"{process.env.FRONTEND_URL}/reset-password?token={reset_token}"
        await email_service.send_password_reset_email(email, reset_url)
        
        return {"message": "If an account exists with this email, a password reset link has been sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error requesting password reset: {str(e)}")

@router.get("/auth/verify-reset-token/{token}")
async def verify_reset_token(token: str):
    """Verify if a password reset token is valid."""
    try:
        is_valid = await db.verify_reset_token(token)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        return {"message": "Token is valid"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying reset token: {str(e)}")

@router.post("/auth/reset-password/{token}")
async def reset_password(token: str, new_password: str):
    """Reset password using a valid reset token."""
    try:
        # Verify token and get user
        user_id = await db.get_user_id_by_reset_token(token)
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
        # Hash new password
        hashed_password = hash_password(new_password)
        
        # Update password in DynamoDB
        await db.update_password(user_id, hashed_password)
        
        # Invalidate reset token
        await db.invalidate_reset_token(token)
        
        return {"message": "Password has been reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting password: {str(e)}") 