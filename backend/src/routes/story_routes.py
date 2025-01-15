from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from ..services.auth_service import AuthService
from ..services.dynamodb_service import DynamoDBService
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
auth_service = AuthService()
db_service = DynamoDBService()

@router.post("/stories")
async def create_story(
    story_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(auth_service.get_current_user)
) -> Dict[str, Any]:
    """
    Create a new story and save it to DynamoDB.
    """
    try:
        story_id = str(uuid.uuid4())
        
        # Prepare story item for DynamoDB
        story_item = {
            'PK': f'STORY#{story_id}',
            'SK': f'STORY#{story_id}',
            'id': story_id,
            'content': story_data.get('content'),
            'prompt': story_data.get('prompt'),
            'author_id': current_user.get('user_id'),  # Get from JWT token
            'status': story_data.get('status', 'draft'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Save to DynamoDB
        await db_service.create_story(story_item)
        
        return {
            'id': story_id,
            'message': 'Story created successfully'
        }
        
    except Exception as e:
        logger.error(f"Error creating story: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create story: {str(e)}"
        ) 