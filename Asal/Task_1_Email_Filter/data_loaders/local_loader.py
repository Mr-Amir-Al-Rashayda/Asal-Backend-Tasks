from .loader_base import EmailLoader, EmailDict
from typing import List
from email_data import EMAILS # This class now handles the import

class LocalFileLoader(EmailLoader):
    """Loads emails from the local mock file (email_data.py)."""
    
    def load_emails(self) -> List[EmailDict]:
        print("Using local mock file...")
        return EMAILS
