import sys
import os # For clearing screen (optional flair)
from .writer_base import BaseWriter, EmailDict, List

class TerminalWriter(BaseWriter):
    """Writes the report to the standard output (terminal)."""
    
    def write_report(self):
        if not self.emails:
            print("No emails found for this choice.")
            return

        print(f"Total emails found: {len(self.emails)}")
        print("-" * 80)
        
        self._write_to_stream(sys.stdout)
        
    def _write_to_stream(self, stream):
        """Helper to print formatted lines to a given stream."""
        # Fixed-width columns for alignment: ID (4), Sender (25), then Subject (variable)
        id_header = "ID".ljust(4)
        sender_header = "Sender".ljust(25)
        stream.write(f"{id_header} | {sender_header} | Subject\n")
        stream.write("-" * 80 + "\n")
        
        for mail in self.emails:
            # Uses private formatting logic for terminal output
            line = self._format_aligned_line(mail) 
            stream.write(line + "\n")

    def _format_aligned_line(self, email):
        """Re-implementation of the basic terminal formatting helper."""
        mail_id = email.get('id', 'N/A')
        sender = email.get('sender', 'N/A')
        subject = email.get('subject', 'No Subject')

        # Fixed-width alignment: ID (4), Sender (25); Subject is full
        id_formatted = str(mail_id).ljust(4)
        sender_formatted = sender[:25].ljust(25)
        return f"{id_formatted} | {sender_formatted} | {subject}"
