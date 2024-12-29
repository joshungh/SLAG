from typing import Dict, List
import json
from src.core.models.story_bible import StoryBible
from src.core.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

class ValidationService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def check_cohesiveness(self, bible: StoryBible) -> Dict[str, List[str]]:
        """Check story bible for inconsistencies and potential issues"""
        system_prompt = """You are a story consistency expert. Analyze this story bible for:
        1. Timeline inconsistencies
        2. Character motivation conflicts
        3. World-building contradictions
        4. Logic gaps in technology or systems
        5. Faction relationship inconsistencies

        Return a JSON response in this format:
        {
            "inconsistencies": [
                {"type": "timeline", "description": "...", "suggestion": "..."},
                // etc
            ],
            "gaps": [
                {"element": "character_motivation", "description": "...", "suggestion": "..."},
                // etc
            ]
        }"""

        bible_json = bible.model_dump_json()
        full_prompt = f"{system_prompt}\n\nStory Bible:\n{bible_json}"
        
        response = await self.llm.generate(full_prompt)
        return json.loads(response)

    async def fix_inconsistencies(self, bible: StoryBible, issues: Dict) -> StoryBible:
        """Apply fixes to identified issues"""
        system_prompt = """You are a story consistency expert. Given the current story bible 
        and identified issues, provide an updated version that resolves these inconsistencies 
        while maintaining the core narrative elements. Return the complete, updated story bible 
        in the same JSON format."""

        prompt = f"""Story Bible:\n{bible.model_dump_json()}\n\nIdentified Issues:\n{json.dumps(issues, indent=2)}"""
        
        response = await self.llm.generate(prompt)
        updated_bible = StoryBible(**json.loads(response))
        return updated_bible 