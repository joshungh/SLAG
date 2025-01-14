from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import bcrypt
from ..services.auth_service import AuthService
from ..services.dynamodb_service import DynamoDBService
from ..models.user import UserCreate, UserLogin, UserResponse, UserUpdate, LoginMethod

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()
db = DynamoDBService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current authenticated user."""
    try:
        return await auth_service.verify_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/register", response_model=Dict[str, Any])
async def register_user(user_data: UserCreate):
    """Register a new user."""
    try:
        return await auth_service.register_email_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(login_data: UserLogin):
    """Login with email and password."""
    try:
        # Get user by email
        user = await db.get_user_by_email(login_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Verify password
        if not bcrypt.checkpw(login_data.password.encode(), user['password'].encode()):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generate token
        user_id = user['PK'].split('#')[1]
        token = auth_service._generate_token(user_id, "email")

        # Remove password from response
        if 'password' in user:
            del user['password']

        return {
            "user": user,
            "token": token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verify")
async def verify_token(user: Dict[str, Any] = Depends(get_current_user)):
    """Verify JWT token and return user data."""
    return {"user": user}

@router.post("/login/google", response_model=Dict[str, Any])
async def login_google(login_data: UserLogin):
    """Login with Google OAuth."""
    try:
        if login_data.login_method != LoginMethod.GOOGLE:
            raise ValueError("Invalid login method for this endpoint")
        return await auth_service.login_google_user(login_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/login/web3", response_model=Dict[str, Any])
async def login_web3(login_data: UserLogin):
    """Login with Web3 wallet."""
    try:
        if login_data.login_method != LoginMethod.WEB3:
            raise ValueError("Invalid login method for this endpoint")
        return await auth_service.login_web3_user(login_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_user_info(
    update_data: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update current user information."""
    try:
        user_id = current_user['PK'].split('#')[1]
        updated_user = await auth_service.db.update_user(user_id, update_data.dict(exclude_unset=True))
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 