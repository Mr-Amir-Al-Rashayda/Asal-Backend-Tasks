from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

# --- The "Base" Class ---
# All our models (tables) will inherit from this class.
# It's the central registry for our schema.
Base = declarative_base()


class Email(Base):
    """
    Defines the 'emails' table schema.
    SQLAlchemy will map this class to the table.
    """
    
    # --- Table Configuration ---
    __tablename__ = 'emails'
    
    # --- Column Definitions ---
    # We'll map our old EmailDict keys to new SQL columns.
    
    # 'id' (Integer, Primary Key)
    # primary_key=True means this value is unique and auto-increments.
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 'sender' (String)
    # String(255) is a good default for email addresses or names.
    sender = Column(String(255), nullable=False)
    
    # 'subject' (String)
    subject = Column(String(255), default="No Subject")
    
    # 'body_snippet' (Text)
    # We use 'Text' instead of 'String' for longer content
    # (like an email body) with no fixed length limit.
    body_snippet = Column(Text, nullable=True)
    
    # 'status' (String)
    # String(50) is fine for "UNREAD", "READ", "LIVE_FETCHED", etc.
    status = Column(String(50), default="UNREAD", index=True)
    
    # 'days_ago' (Integer)
    # We will store this as a calculated number.
    days_ago = Column(Integer, default=0)
    
    # 'received_at' (DateTime)
    # It's best practice to store the *actual* timestamp.
    # 'default=datetime.utcnow' sets the timestamp when the row is created.
    received_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        """A helper method to make printing Email objects look nice."""
        return f"<Email(id={self.id}, from='{self.sender}', subject='{self.subject}')>"

# --- A small main block to create the table ---
# This part will only run when you execute `python models.py`

if __name__ == "__main__":
    # We import the engine from our *working* db_config file
    try:
        from db_config import engine 
        
        print("Connecting to the database to create tables...")
        
        # This is the magic command:
        # It checks the database. If the 'emails' table doesn't exist,
        # it creates it based on the 'Email' class definition above.
        Base.metadata.create_all(engine)
        
        print("✅ Tables created successfully (if they didn't already exist).")
        
    except ImportError:
        print("ERROR: Could not import 'engine' from db_config.py.")
        print("Please ensure db_config.py exists and is configured correctly.")
    except Exception as e:
        print(f"ERROR: An error occurred while creating tables.")
        print(f"Details: {e}")