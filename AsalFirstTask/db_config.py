from sqlalchemy import create_engine
import os

# --- Your Live Connection String ---
# We've filled this in with the details you provided.
#
# User:     root
# Password: AmirRashaydaamir123sq
# Host:     From environment variable (DB_HOST) or 'localhost' by default
# Database: my_email_project  <-- (From Step 1 above)
#
# Get DB host from environment (Docker passes 'host.docker.internal')
# If not in Docker, default to 'localhost'
db_host = os.getenv('DB_HOST', 'localhost')
DATABASE_URL = f"mysql+pymysql://root:AmirRashaydaamir123sq@{db_host}/my_email_project"


# The Engine is the central source of connectivity to the database.
engine = create_engine(DATABASE_URL, echo=False)

# Test the connection only when this file is run directly
if __name__ == "__main__":
    try:
        print("Attempting to connect to MySQL database...")
        # Test the connection
        with engine.connect() as connection:
            print("[OK] Connection to MySQL database successful!")
            print(f"[OK] Connected to database: my_email_project")
            
    except ImportError as e:
        print("[ERROR] Required library not found.")
        print(f"Details: {e}")
        print("Please install PyMySQL by running: pip install PyMySQL")
    except Exception as e:
        print(f"[ERROR] Could not connect to the database.")
        print(f"Details: {e}")
        print("\n--- Troubleshooting ---")
        print("1. Is your MySQL server running?")
        print("2. Did you create the 'my_email_project' database?")
        print("3. Is your username/password correct in the DATABASE_URL?")
        print("4. Try running: net start mysql (on Windows) to start MySQL service")