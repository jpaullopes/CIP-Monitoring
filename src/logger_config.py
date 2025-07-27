# logger_config.py
import logging
import colorlog

def setup_logger(name: str = __name__) -> logging.Logger:
    """Configure and return a colored logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler()
    
    # Define colored formatter using colorlog
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        },
        secondary_log_colors={},
        style='%'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger
