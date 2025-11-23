from typing import List, Dict, Any

EmailDict = Dict[str, Any]

class Mailbox:
    """
    Handles encapsulation of email data and provides methods for filtering.
    """
    
    def __init__(self, emails: List[EmailDict]):
        # Stores a safe shallow copy of the list to protect the original data source.
        self.emails: List[EmailDict] = emails[:]
    
    def filter_unread(self) -> List[EmailDict]:
        """Returns a list of UNREAD emails."""
        # Using a generic status check suitable for mock or real data
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