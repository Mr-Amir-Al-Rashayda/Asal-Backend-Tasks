import pika
import json
import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# --- Import your EXISTING project files ---
from data_loaders import GmailLoader, DatabaseLoader
from schemas import EmailCreate


@dataclass
class GmailCredentials:
    """Data class to hold Gmail credentials (Single Responsibility: Data Structure)"""
    username: str
    password: str


class MessageParser:
    """Single Responsibility: Parse and validate messages from RabbitMQ"""
    
    @staticmethod
    def parse_sync_request(body: bytes) -> Optional[GmailCredentials]:
        """
        Parse JSON message body and extract Gmail credentials.
        Returns None if parsing fails or credentials are invalid.
        """
        try:
            sync_data = json.loads(body.decode())
            username = sync_data.get("username")
            app_password = sync_data.get("app_password")
            
            if not username or not app_password:
                print("❌ ERROR: Missing username or app_password in request.")
                return None
            
            return GmailCredentials(username=username, password=app_password)
            
        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Failed to parse JSON from message: {e}")
            return None
        except Exception as e:
            print(f"❌ ERROR: Failed to extract credentials: {e}")
            return None


class GmailFetcher:
    """Single Responsibility: Fetch emails from Gmail"""
    
    def __init__(self, credentials: GmailCredentials, count: int = 10):
        self.credentials = credentials
        self.count = count
    
    def fetch_emails(self) -> List[Dict[str, Any]]:
        """
        Fetch emails from Gmail using GmailLoader.
        Returns empty list if fetching fails.
        """
        print(f" [ ] Contacting Gmail as {self.credentials.username}...")
        try:
            gmail_loader = GmailLoader(
                username=self.credentials.username,
                password=self.credentials.password,
                count=self.count
            )
            fetched_emails = gmail_loader.load_emails()
            return fetched_emails if fetched_emails else []
        except Exception as e:
            print(f"FAILED to fetch from Gmail: {e}")
            return []


class EmailSaver:
    """Single Responsibility: Save emails to database"""
    
    @staticmethod
    def save_email(email_dict: Dict[str, Any]) -> bool:
        """
        Save a single email to the database.
        Returns True if successful, False otherwise.
        """
        try:
            db_loader = DatabaseLoader()
            email_schema = EmailCreate(**email_dict)
            db_loader.create_email(email_schema)
            print(f" [✓] Saved email from {email_schema.sender}")
            return True
        except Exception as e:
            print(f"FAILED to save email {email_dict.get('subject')}: {e}")
            return False
    
    @staticmethod
    def save_all_emails(emails: List[Dict[str, Any]]) -> int:
        """
        Save multiple emails to the database.
        Returns the number of successfully saved emails.
        """
        if not emails:
            return 0
        
        print(f" [ ] Fetched {len(emails)} emails. Saving to database...")
        saved_count = 0
        
        for email_dict in emails:
            if EmailSaver.save_email(email_dict):
                saved_count += 1
        
        return saved_count


class GmailSyncProcessor:
    """
    Orchestrator class that coordinates the Gmail sync process.
    Follows Single Responsibility: Orchestrates the sync workflow.
    """
    
    def __init__(self, credentials: GmailCredentials, email_count: int = 10):
        self.credentials = credentials
        self.fetcher = GmailFetcher(credentials, email_count)
        self.saver = EmailSaver()
    
    def process(self) -> bool:
        """
        Execute the complete Gmail sync process.
        Returns True if at least one email was processed, False otherwise.
        """
        # Step 1: Fetch emails from Gmail
        fetched_emails = self.fetcher.fetch_emails()
        
        if not fetched_emails:
            print(" [✓] No new emails fetched from Gmail. Job complete.")
            return False
        
        # Step 2: Save emails to database
        saved_count = self.saver.save_all_emails(fetched_emails)
        
        print(f" [x] Gmail sync job finished. Saved {saved_count}/{len(fetched_emails)} emails.")
        return saved_count > 0


def process_gmail_sync(ch, method, properties, body):
    """
    Main callback function for RabbitMQ message processing.
    Single Responsibility: Handle message acknowledgment and error recovery.
    Delegates actual work to specialized classes.
    """
    print("\n---")
    print(f" [x] Received job: {body.decode()}")
    
    # Step 1: Parse the message (Single Responsibility: Parsing)
    credentials = MessageParser.parse_sync_request(body)
    if not credentials:
        # Acknowledge message even if parsing fails (to prevent infinite retries)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    print(f" [✓] Extracted credentials for user: {credentials.username}")
    
    # Step 2: Process the sync (Single Responsibility: Orchestration)
    try:
        processor = GmailSyncProcessor(credentials, count=10)
        processor.process()
        # Acknowledge message only after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"❌ CRITICAL ERROR during sync processing: {e}")
        # In production, you might want to use basic_nack with requeue=True
        # For now, we acknowledge to prevent infinite retries of bad messages
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    print("---")

# --- This is the "receiver" logic from receive.py ---
def main():
    """
    Main function to start the RabbitMQ consumer.
    Single Responsibility: Initialize connection and start consuming messages.
    """
    try:
        # Get the hostname from Environment, default to 'localhost' for testing
        rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host))
    except pika.exceptions.AMQPConnectionError:
        print("❌ FAILED to connect to RabbitMQ. Is it running? (docker run ...)")
        return
        
    channel = connection.channel()
    channel.queue_declare(queue='gmail_sync_queue', durable=True)  # Durable queue survives restarts
    
    # Set quality of service: process one message at a time
    # This ensures fair distribution of work among multiple workers
    channel.basic_qos(prefetch_count=1)

    # Tell RabbitMQ to call our 'process_gmail_sync' function for the queue
    # auto_ack=False means we manually acknowledge messages (better reliability)
    channel.basic_consume(
        queue='gmail_sync_queue',
        on_message_callback=process_gmail_sync,
        auto_ack=False  # Manual acknowledgment for better error handling
    )

    print(' [*] Waiting for jobs on queue "gmail_sync_queue". To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('\n [*] Stopping worker...')
        channel.stop_consuming()
        connection.close()
        print(' [*] Worker stopped gracefully.')

if __name__ == '__main__':
    main()