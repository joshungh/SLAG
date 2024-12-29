import logging
import sys
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with consistent formatting
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Avoid adding handlers multiple times
        logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # Ensure logs directory exists
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f'test_{datetime.now().strftime("%Y%m%d")}.log')
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Create formatters and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger 