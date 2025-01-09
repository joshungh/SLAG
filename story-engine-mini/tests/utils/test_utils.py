import os
import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def validate_story_files(output_dir: str, required_files: list) -> None:
    """Validate story output files exist and aren't empty"""
    for file in required_files:
        file_path = f'{output_dir}/{file}'
        if not os.path.exists(file_path):
            raise AssertionError(f"Missing file: {file}")
        if os.path.getsize(file_path) == 0:
            raise AssertionError(f"Empty file: {file}")

def validate_story_context(context: Dict) -> None:
    """Validate story context has required fields"""
    required_fields = ['story_id', 'namespace', 'output_dir', 'current_phase']
    for field in required_fields:
        if field not in context:
            raise AssertionError(f"Missing {field} in context")
        if not context[field]:
            raise AssertionError(f"Empty {field} in context") 