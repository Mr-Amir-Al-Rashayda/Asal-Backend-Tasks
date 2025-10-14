from typing import List, Dict, Any

# Define a type alias for readability
EmailDict = Dict[str, Any]

# Imports the raw data from email_data.py 
from email_data import EMAILS 

class Mailbox:
    """
    Handles encapsulation of email data and provides methods for filtering.
    """
    
    def __init__(self, emails: List[EmailDict]):
        self.emails: List[EmailDict] = emails[:]
    
    def filter_unread(self) -> List[EmailDict]:
        """Returns a list of UNREAD emails."""
        return [email for email in self.emails if email.get('status') == "UNREAD"]

    def filter_last_day(self) -> List[EmailDict]:
        """Returns emails received today (0 days ago)."""
        return [email for email in self.emails if email.get('days_ago') == 0]

    def filter_last_one(self) -> List[EmailDict]:
        """Returns the single most recent email as a list (maintaining uniform interface)."""
        if self.emails:
            return [self.emails[-1]] 
        return []

    def filter_all(self) -> List[EmailDict]:
        """Returns a SAFE shallow copy of all emails."""
        return self.emails[:]