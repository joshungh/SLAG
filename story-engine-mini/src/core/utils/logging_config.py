import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(output_dir: str = 'output/logs'):
    """
    Configure logging with rotation
    
    Args:
        output_dir: Directory for log files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    log_file = f'{output_dir}/story_service.log'
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,  # 10MB
        backupCount=5,        # Keep 5 backup files
        encoding='utf-8'
    )
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Create story-specific log
    story_logger = logging.getLogger('story_service')
    story_logger.setLevel(logging.DEBUG)
    
    return story_logger 