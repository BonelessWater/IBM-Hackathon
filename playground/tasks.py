import logging
from .utils import fetch_and_log_emails  # Import your email logging function

logger = logging.getLogger(__name__)

def log_emails_task():
    try:
        fetch_and_log_emails()
        logger.info("Successfully logged emails.")
    except Exception as e:
        logger.error(f"Error logging emails: {str(e)}")
