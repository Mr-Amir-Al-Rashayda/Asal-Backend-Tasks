from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# This is our "base" model. It contains all the common fields.
class EmailBase(BaseModel):
    sender: str
    subject: Optional[str] = "No Subject"
    body_snippet: Optional[str] = None
    status: Optional[str] = "UNREAD"
    days_ago: Optional[int] = 0

# This is the model we use when CREATING a new email (for POST)
# It's the same as the base for this simple example.
class EmailCreate(EmailBase):
    pass

# This is the model we use when UPDATING an email (for PUT)
# All fields are optional, so a user can update just one thing (e.g., status).
class EmailUpdate(BaseModel):
    sender: Optional[str] = None
    subject: Optional[str] = None
    body_snippet: Optional[str] = None
    status: Optional[str] = None
    days_ago: Optional[int] = None

# This is the model we use when RESPONDING to a request.
# It includes the 'id' and 'received_at' from the database.
class EmailResponse(EmailBase):
    id: int
    received_at: datetime

    class Config:
        # This tells Pydantic to read data from our SQLAlchemy model
        from_attributes = True
        
        
class GmailSyncRequest(BaseModel):
    username: str
    app_password: str