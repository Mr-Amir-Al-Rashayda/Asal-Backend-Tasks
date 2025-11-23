# FILE: api.py

import pika
import json
import os
from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
# Import our schemas
from schemas import EmailCreate, EmailUpdate, EmailResponse, EmailBase, GmailSyncRequest
# Import BOTH loaders now
from data_loaders import DatabaseLoader, LocalFileLoader
import csv
from io import StringIO
from fastapi.responses import StreamingResponse # Used for the CSV response

# 1. Initialization
app = FastAPI(
    title="Email Processing API",
    description="A REST API to filter and read emails from a database.",
    version="1.0.0"
)

def get_loader():
    return DatabaseLoader()

# --- 2. Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome to the Email API. Go to /docs for documentation."}

# --- Database CRUD Endpoints ---

@app.post("/emails", response_model=EmailResponse, status_code=status.HTTP_201_CREATED, tags=["Database Emails"])
def create_new_email(email_to_create: EmailCreate):
    """(C) Creates a new email in the database."""
    loader = get_loader()
    new_email = loader.create_email(email_to_create)
    if not new_email:
        raise HTTPException(status_code=400, detail="Error creating email")
    return new_email

@app.get("/emails/all", response_model=List[EmailResponse], tags=["Database Emails"])
def get_all_emails():
    """(R) Fetches all emails from the database."""
    loader = get_loader()
    return loader.load_emails()

@app.get("/emails/unread", response_model=List[EmailResponse], tags=["Database Emails"])
def get_unread_emails():
    """(R) Fetches only unread emails from the database."""
    loader = get_loader()
    return loader.load_unread_emails()

@app.get("/emails/today", response_model=List[EmailResponse], tags=["Database Emails"])
def get_emails_from_today():
    """(R) Fetches emails from the last day from the database."""
    loader = get_loader()
    return loader.load_emails_last_day()

@app.get("/email/{email_id}", response_model=EmailResponse, tags=["Database Emails"])
def get_email_by_id(email_id: int):
    """(R) Fetches a single email by its unique ID."""
    loader = get_loader()
    email = loader.load_email_by_id(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

# --- NEW ENDPOINT (from main.py Filter 3) ---
@app.get("/emails/latest", response_model=EmailResponse, tags=["Database Emails"])
def get_latest_email():
    """(R) Fetches the single most recent email from the database."""
    loader = get_loader()
    email = loader.load_latest_email()
    if not email:
        raise HTTPException(status_code=404, detail="No emails found")
    return email

@app.put("/email/{email_id}", response_model=EmailResponse, tags=["Database Emails"])
def update_existing_email(email_id: int, email_to_update: EmailUpdate):
    """(U) Updates an existing email."""
    loader = get_loader()
    updated_email = loader.update_email(email_id, email_to_update)
    if not updated_email:
        raise HTTPException(status_code=404, detail="Email not found or could not be updated")
    return updated_email

@app.delete("/email/{email_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Database Emails"])
def delete_existing_email(email_id: int):
    """(D) Deletes an email by its unique ID."""
    loader = get_loader()
    success = loader.delete_email(email_id)
    if not success:
        raise HTTPException(status_code=404, detail="Email not found")
    return None

# --- NEW ENDPOINT (from main.py Data Choice 1) ---
@app.get("/local/emails", response_model=List[EmailBase], tags=["Local Mock Data"])
def get_local_emails():
    """
    (R) Fetches all emails from the local mock file (email_data.py).
    This replaces 'Choice 1: Use Local Mock File' from main.py.
    """
    loader = LocalFileLoader()
    return loader.load_emails()

# --- NEW ENDPOINT (from main.py Output Choice) ---
@app.get("/reports/all/csv", tags=["Reports"])
def get_all_emails_csv_report():
    """
    (R) Generates a CSV report of all emails from the database.
    This replaces the 'Output Choice' logic from main.py.
    """
    loader = get_loader()
    emails = loader.load_emails() # This returns a List[Email]
    
    # Use StringIO to create an in-memory file for the CSV
    stream = StringIO()
    writer = csv.writer(stream)
    
    # Write Header
    writer.writerow(['id', 'sender', 'subject', 'status', 'days_ago', 'received_at'])
    
    # Write Data
    for email in emails:
        writer.writerow([
            email.id,
            email.sender,
            email.subject,
            email.status,
            email.days_ago,
            email.received_at
        ])
    
    # Go back to the start of the in-memory file
    stream.seek(0)
    
    # Create a streaming response
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    # This header tells the browser to download the file
    response.headers["Content-Disposition"] = "attachment; filename=all_emails_report.csv"
    return response



@app.post("/sync/gmail", status_code=status.HTTP_202_ACCEPTED, tags=["Gmail Sync"])
def request_gmail_sync(sync_request: GmailSyncRequest): # <-- 3. Accept the new model
    """
    Requests a new sync from Gmail using credentials from the request body.
    *** WARNING: THIS IS INSECURE FOR PRODUCTION. ***
    """
    try:
        # Get the hostname from Environment, default to 'localhost' for testing
        rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
        channel = connection.channel()
        channel.queue_declare(queue='gmail_sync_queue', durable=True)  # Durable queue survives restarts

        # 4. Convert the incoming Pydantic model to a JSON string
        message_body = sync_request.model_dump_json()
        
        channel.basic_publish(
            exchange='',
            routing_key='gmail_sync_queue',
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent (survives RabbitMQ restarts)
            )
        )

        connection.close()
        return {"message": "Accepted: Gmail sync job has been queued."}
        
    except pika.exceptions.AMQPConnectionError:
        raise HTTPException(status_code=503, detail="Service Unavailable: Could not connect to message broker.")
    