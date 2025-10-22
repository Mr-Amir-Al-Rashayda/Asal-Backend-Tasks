import imaplib
import email
from typing import List, Dict, Any, Optional
import ssl 
from email.header import decode_header
from email.message import Message
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

EmailDict = Dict[str, Any]

class GmailFetcher:
    """
    Handles connection, authentication, and fetching of emails from a Gmail account 
    using the IMAP protocol.
    """
    
    GMAIL_IMAP_SERVER = "imap.gmail.com"
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.mail: Optional[imaplib.IMAP4_SSL] = None
        
    def connect_and_fetch(self, count: int = 10) -> List[EmailDict]:
        """Connects to Gmail, fetches the latest emails, and returns them as EmailDict objects."""
        fetched_emails: List[EmailDict] = []
        
        print(f"Attempting to connect to Gmail ({self.GMAIL_IMAP_SERVER})...")

        try:
            self._connect()

            mail_ids = self._search_all_ids()
            latest_ids = mail_ids[-count:][::-1]

            for email_id in latest_ids:
                raw = self._fetch_raw_message(email_id)
                if not raw:
                    continue
                msg = email.message_from_bytes(raw)
                fetched_emails.append(self._build_email_record(email_id, msg))

            print(f"SUCCESS: Fetched {len(fetched_emails)} emails from Gmail.")
            return fetched_emails

        except imaplib.IMAP4.error as e:
            print(f"ERROR: Gmail login failed. Check credentials, App Password, and IMAP settings. Details: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
        finally:
            self._disconnect()
    
    def _connect(self) -> None:
        self.mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP_SERVER)
        self.mail.login(self.username, self.password)
        self.mail.select('inbox')

    def _disconnect(self) -> None:
        if self.mail:
            try:
                self.mail.logout()
            finally:
                self.mail = None

    #  Fetch flow building blocks
    def _search_all_ids(self) -> List[bytes]:
        assert self.mail is not None
        status, data = self.mail.search(None, 'ALL')
        if status != 'OK' or not data:
            return []
        return data[0].split()

    def _fetch_raw_message(self, email_id: bytes) -> Optional[bytes]:
        assert self.mail is not None
        status, msg_data = self.mail.fetch(email_id, '(RFC822)') # Fetches the raw content of one specific email by its ID using the standard format.
        if status != 'OK' or not msg_data:
            return None
        return msg_data[0][1]

    def _build_email_record(self, email_id: bytes, msg: Message) -> EmailDict:
        days_ago_value = self._compute_days_ago(msg)
        return {
            "id": int(email_id.decode()),
            "sender": self._decode_header_to_str(msg['From']),
            "subject": self._decode_header_to_str(msg['Subject']),
            "body_snippet": "Live email bodies require advanced MIME parsing (omitted).",
            "status": "LIVE_FETCHED",
            "days_ago": days_ago_value if days_ago_value is not None else "N/A",
        }

    def _compute_days_ago(self, msg: Message) -> Optional[int]:
        try:
            date_header = msg.get('Date')
            if not date_header:
                return None
            received_dt = parsedate_to_datetime(date_header)
            if received_dt.tzinfo is None:
                received_dt = received_dt.replace(tzinfo=timezone.utc)
            local_received = received_dt.astimezone()
            local_today = datetime.now(local_received.tzinfo)
            return (local_today.date() - local_received.date()).days
        except Exception:
            return None
        
    # Parsing helpers
    def _decode_header_to_str(self, header_value: Optional[str]) -> str:
        return str(email.header.make_header(decode_header(header_value))) if header_value else ""
