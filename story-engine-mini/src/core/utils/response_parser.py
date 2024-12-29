import json
from typing import Dict, Any

class ResponseParser:
    @staticmethod
    def parse_json_response(response: str) -> Dict[str, Any]:
        """
        Parse JSON response from Claude, handling potential formatting issues
        """
        try:
            # Find the first '{' and last '}' to extract JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Claude's response as JSON: {str(e)}") 