from typing import List, Dict, Any

# Define a type alias for readability
EmailDict = Dict[str, Any]

class ReportGenerator:
    """
    Handles all responsibility related to formatting and printing output (I/O).
    """
    

    def print_report(self, filtered_emails: List[EmailDict], title: str):
        """[Public I/O] Handles only the output to the terminal."""
        print("\n" + "-" * 80)
        print(f"REPORT FOR: {title}")
        print(f"Total emails found: {len(filtered_emails)}")
        print("-" * 80)
        
        if not filtered_emails:
            print("No emails found for this choice.")
            return

        print("ID   | Sender (First 25 chars)         | Subject (First 40 chars)")
        print("-" * 80)
        
        for mail in filtered_emails:
            display_line = self._format_email_line(mail) 
            print(display_line)

    def _format_email_line(self, email: EmailDict) -> str:
        """[Private Process] Takes raw email data and formats it into a single aligned string (using F-strings)."""
        mail_id = email.get('id', 'N/A')
        sender = email.get('sender', 'N/A')
        subject = email.get('subject', 'No Subject')
        
        sender_formatted = self._pad_string_basic(sender, 25)
        subject_formatted = self._pad_string_basic(subject, 40)
        
        # Uses efficient F-strings 
        return f"{mail_id}    | {sender_formatted} | {subject_formatted}"

    def _pad_string_basic(self, text: str, target_length: int) -> str:
        """[Private Helper] Manually pads a string with spaces."""
        short_text = text[:target_length]
        spaces_needed = target_length - len(short_text)
        padding = " " * spaces_needed
        return short_text + padding