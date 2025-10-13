from email_data import EMAILS 

class Mailbox:
    """
    Handles encapsulation of email data and provides methods for filtering.
    All filter methods uses List Comprehensions.
    """
    def __init__(self, email_list):
        self.emails = email_list

    def filter_unread(self):
        """Returns a list of UNREAD emails using a list comprehension."""
        return [email for email in self.emails if email.get('status') == "UNREAD"]

    def filter_last_day(self):
        """Returns emails received today (0 days ago) using a list comprehension."""
        return [email for email in self.emails if email.get('days_ago') == 0]

    def filter_last_one(self):
        """Returns the single most recent email."""
        if self.emails:
            return [self.emails[-1]] 
        return []

    def filter_all(self):
        """
        Returns a SAFE copy of all emails. 
        """
        return self.emails[:]

class ReportGenerator:
    """
    Handles all responsibility related to formatting and printing output 
    to the terminal (I/O). All formatting logic is marked as private (_).
    """

    def _pad_string_basic(self, text, target_length):
        """[Private Helper] Manually pads a string with spaces."""
        short_text = text[:target_length]
        spaces_needed = target_length - len(short_text)
        padding = " " * spaces_needed
        return short_text + padding

    def _format_email_line(self, email):
        """[Private Process] Takes raw email data and formats it into a single aligned string."""
        mail_id = email.get('id', 'N/A')
        sender = email.get('sender', 'N/A')
        subject = email.get('subject', 'No Subject')
        
        sender_formatted = self._pad_string_basic(sender, 25)
        subject_formatted = self._pad_string_basic(subject, 40)
        
        return str(mail_id) + "    | " + sender_formatted + " | " + subject_formatted

    def print_report(self, filtered_emails, title):
        """[Public I/O] Handles only the output to the terminal."""
        # 1. Print Header
        print("\n" + "-" * 80)
        print(f"REPORT FOR: {title}")
        print(f"Total emails found: {len(filtered_emails)}")
        
        if not filtered_emails:
            print("No emails found for this choice.")
            return

        print("--------------------------------------------------------------------------------")
        print("ID   | Sender (First 25 chars)         | Subject (First 40 chars)")
        print("--------------------------------------------------------------------------------")
        
        # 2. Print Email Lines - uses the formatting helper
        for mail in filtered_emails:
            display_line = self._format_email_line(mail) 
            print(display_line)


FILTER_FUNCTIONS = {
    "1": Mailbox.filter_unread,
    "2": Mailbox.filter_last_day,
    "3": Mailbox.filter_last_one,
    "4": Mailbox.filter_all,
}

FILTER_TITLES = {
    "1": "UNREAD EMAILS",
    "2": "EMAILS FROM THE LAST DAY (TODAY)",
    "3": "THE LAST ONE RECEIVED",
    "4": "ALL EMAILS",
}

def run_email_processor(mailbox_instance, report_instance):
    """Manages the program loop and user interaction."""
    while True:
        print("\n" + "=" * 50)
        print("EMAIL FILTERING CHOICES:")
        for key, title in FILTER_TITLES.items():
            print(f"{key}: View {title}")
        print("0: Exit Program")
        print("=" * 50)
        
        choice = input("Enter your choice (1, 2, 3, 4, or 0): ")
        
        if choice == "0":
            print("Exiting the program. Goodbye!")
            break
        
        handler_func = FILTER_FUNCTIONS.get(choice)

        if handler_func:
            filtered_emails = handler_func(mailbox_instance)
            
            title = FILTER_TITLES.get(choice) 

            report_instance.print_report(filtered_emails, title)
            
            input("\nPress Enter to see the choices again...")
            
        else:
            print("Invalid choice. Please enter a number from the list.")
            continue


if __name__ == "__main__":
    email_data = EMAILS 
    
    mailbox = Mailbox(email_data)
    reporter = ReportGenerator()
    
    run_email_processor(mailbox, reporter)
