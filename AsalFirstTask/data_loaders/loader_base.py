from abc import ABC, abstractmethod
from typing import List, Dict, Any

EmailDict = Dict[str, Any]

class EmailLoader(ABC):
    """
    Abstract Base Class (Interface) for all data sources.
    Guarantees that every loader implements a load_emails method.
    """
    @abstractmethod
    def load_emails(self) -> List[EmailDict]:
        """
        Subclasses MUST implement this method to fetch/load email data.
        """
        raise NotImplementedError("Subclasses must implement the load_emails method.")
