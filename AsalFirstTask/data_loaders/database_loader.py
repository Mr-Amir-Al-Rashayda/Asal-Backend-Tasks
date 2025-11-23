# FILE: database_loader.py

from sqlalchemy.orm import sessionmaker
from .loader_base import EmailLoader, EmailDict # Keep EmailDict for compatibility
from db_config import engine 
from models import Email     
from schemas import EmailCreate, EmailUpdate # Import our new Pydantic models
from typing import List, Optional

class DatabaseLoader(EmailLoader):
    """
    Loads and MODIFIES emails from the MySQL database via SQLAlchemy.
    """
    
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        print("DatabaseLoader initialized, session created.")

    def _close_session(self):
        """Helper to safely close the session."""
        if self.session:
            self.session.close()

    # READ METHODS
    def load_emails(self) -> List[dict]:
        print("Fetching ALL emails from database...")
        try:
            results = self.session.query(Email).all()
            # We return the Email objects themselves for easier conversion
            return results
        except Exception as e:
            print(f"ERROR: Could not fetch emails: {e}")
            return []
        finally:
            self._close_session()
            
    def load_latest_email(self) -> Optional[Email]:
        """Fetches the single most recent email (by received_at)."""
        print("Fetching latest email from database...")
        try:
            # Order by the 'received_at' column in descending order
            # and get the first one.
            email = self.session.query(Email).order_by(Email.received_at.desc()).first()
            return email
        except Exception as e:
            print(f"ERROR: Could not fetch latest email: {e}")
            return None
        finally:
            self._close_session()

    def load_unread_emails(self) -> List[dict]:
        print("Fetching UNREAD emails from database...")
        try:
            results = self.session.query(Email).filter(Email.status == "UNREAD").all()
            return results
        except Exception as e:
            print(f"ERROR: Could not fetch unread emails: {e}")
            return []
        finally:
            self._close_session()

    def load_emails_last_day(self) -> List[dict]:
        print("Fetching emails from last day...")
        try:
            results = self.session.query(Email).filter(Email.days_ago == 0).all()
            return results
        except Exception as e:
            print(f"ERROR: Could not fetch last day's emails: {e}")
            return []
        finally:
            self._close_session()
            
    def load_email_by_id(self, email_id: int) -> Optional[Email]:
        print(f"Fetching email with id={email_id}...")
        try:
            email = self.session.query(Email).get(email_id) 
            return email
        except Exception as e:
            print(f"ERROR: Could not fetch email by id: {e}")
            return None
        finally:
            self._close_session()

    # NEW: CREATE METHOD
    def create_email(self, email_to_create: EmailCreate) -> Email:
        """Adds a new email to the database."""
        print(f"Creating new email from: {email_to_create.sender}")
        try:
            # Convert Pydantic model to a dictionary
            email_data = email_to_create.model_dump()
            # Create a new SQLAlchemy Email object
            new_email = Email(**email_data)
            
            self.session.add(new_email)
            self.session.commit()
            self.session.refresh(new_email) # Get the new ID from the DB
            return new_email
        except Exception as e:
            print(f"ERROR: Could not create email: {e}")
            self.session.rollback()
            return None
        finally:
            self._close_session()

    # --- NEW: UPDATE METHOD ---
    def update_email(self, email_id: int, email_to_update: EmailUpdate) -> Optional[Email]:
        """Updates an existing email."""
        print(f"Updating email id={email_id}...")
        try:
            # First, get the email from the DB
            db_email = self.session.query(Email).get(email_id)
            if not db_email:
                return None # Email not found
            
            # Convert Pydantic model to a dict, excluding unset fields
            update_data = email_to_update.model_dump(exclude_unset=True)
            
            # Update the fields
            for key, value in update_data.items():
                setattr(db_email, key, value)
                
            self.session.commit()
            self.session.refresh(db_email)
            return db_email
        except Exception as e:
            print(f"ERROR: Could not update email: {e}")
            self.session.rollback()
            return None
        finally:
            self._close_session()

    # --- NEW: DELETE METHOD ---
    def delete_email(self, email_id: int) -> bool:
        """Deletes an email from the database."""
        print(f"Deleting email id={email_id}...")
        try:
            db_email = self.session.query(Email).get(email_id)
            if not db_email:
                return False # Email not found
            
            self.session.delete(db_email)
            self.session.commit()
            return True
        except Exception as e:
            print(f"ERROR: Could not delete email: {e}")
            self.session.rollback()
            return False
        finally:
            self._close_session()