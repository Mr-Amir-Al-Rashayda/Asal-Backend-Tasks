from sqlalchemy.orm import sessionmaker
from db_config import engine # Import our configured engine
from models import Email     # Import our table model
from email_data import EMAILS # Import the mock data list
from datetime import datetime

# 1. Create a Session Factory
# We bind it to our engine, so it knows which database to talk to.
Session = sessionmaker(bind=engine)

# 2. Create an actual session object
session = Session()

print(f"Populating database from 'email_data.py'...")
print(f"Found {len(EMAILS)} mock emails to insert.")

try:
    # 3. Loop through the list of dictionaries
    for email_dict in EMAILS:
        
        # 4. Create an 'Email' *object* from the dictionary
        # This maps our dictionary keys to the Email class attributes
        new_email = Email(
            # Note: We don't provide 'id'; the database auto-generates it.
            sender=email_dict.get('sender'),
            subject=email_dict.get('subject'),
            body_snippet=email_dict.get('body_snippet'),
            status=email_dict.get('status'),
            days_ago=email_dict.get('days_ago'),
            # We'll set a placeholder received_at time for mock data
            received_at=datetime.utcnow() 
        )
        
        # 5. Add the new object to our session (the "staging area")
        session.add(new_email)

    # 6. Commit (save) all staged changes to the database
    # This runs the actual "INSERT" SQL commands
    session.commit()
    print("Success: All emails have been added to the database.")

except Exception as e:
    # If anything goes wrong, roll back all changes
    print(f"ERROR: Could not add emails to database.")
    print(f"Details: {e}")
    session.rollback()
finally:
    # Always close the session when you're done
    session.close()
    print("Session closed.")