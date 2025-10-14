
from mailbox import Mailbox
from report_generator import ReportGenerator
from email_data import EMAILS 

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


def run_email_processor():
    """Manages the program loop and user interaction."""
    
    email_data = EMAILS 
    mailbox = Mailbox(email_data)
    reporter = ReportGenerator()
    print("Email Filter Program Initialized.")
    while True:
        print("\n" + "=" * 50)
        print("EMAIL FILTERING CHOICES:")
        for key, title in FILTER_TITLES.items():
            print(f"{key}: View {title}")
        print("0: Exit Program")
        
        choice = input("Enter your choice (1, 2, 3, 4, or 0): ")
        
        if choice == "0":
            print("Exiting the program. Goodbye!")
            break
        
        # Dictionary Dispatch Logic: Safely retrieves the method to call
        handler_func = FILTER_FUNCTIONS.get(choice)

        if handler_func:
            # Filtering: call the method on the mailbox instance
            filtered_emails = handler_func(mailbox)
            
            # Report Setup
            title = FILTER_TITLES.get(choice) 

            # Printing: call the report method
            reporter.print_report(filtered_emails, title)
            
            input("\nPress Enter to see the choices again...")
            
        else:
            print("Invalid choice. Please enter a number from the choices.")
            continue


if __name__ == "__main__":
    run_email_processor()