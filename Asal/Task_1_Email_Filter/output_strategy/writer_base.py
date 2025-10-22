from abc import ABC, abstractmethod
from typing import List, Dict, Any

EmailDict = Dict[str, Any]

class BaseWriter(ABC):
    """
    Conceptual Base Class (Interface) for all output formats.
    Guarantees that every writer has the data and implements the write_report method.
    """
    def __init__(self, filtered_emails: List[EmailDict], title: str):
        self.emails = filtered_emails
        self.title = title
    
    @abstractmethod
    def write_report(self):
        """
        Subclasses MUST implement this method to handle the specific I/O operation.
        """
        raise NotImplementedError("Subclasses must implement the write_report method.")