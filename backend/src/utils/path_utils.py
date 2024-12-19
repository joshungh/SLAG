import os
from pathlib import Path

def get_project_root() -> Path:
    """Get the absolute path to the project root directory"""
    return Path(__file__).parent.parent.parent

def get_reference_doc_path(relative_path: str) -> str:
    """Get the absolute path to a reference document
    
    Args:
        relative_path: Path relative to reference-documents directory
        
    Returns:
        Absolute path to the document
    """
    root = get_project_root()
    full_path = root / "src" / "reference-documents" / relative_path
    return str(full_path.resolve()) 