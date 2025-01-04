from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Story(BaseModel):
    title: str
    author: str = "AI Story Engine"
    genre: str
    content: str
    created_at: datetime = datetime.now()
    word_count: int
    framework_id: str  # reference to framework used
    bible_id: str     # reference to story bible used 