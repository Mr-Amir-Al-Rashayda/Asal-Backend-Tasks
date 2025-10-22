
from mailbox import Mailbox
from report_generator import ReportGenerator 
from email_data import EMAILS # Still needed for the Local File option
from data_fetcher import GmailFetcher # NEW: Import the Gmail connector
from typing import List, Dict, Any 


# Maps user input (1-4) to the Mailbox filtering method
FILTER_FUNCTIONS = {
    "1": Mailbox.filter_unread,
    "2": Mailbox.filter_last_day,
    "3": Mailbox.filter_last_one,
    "4": Mailbox.filter_all,
}

# Maps user input (1-4) to the correct report title string
FILTER_TITLES = {
    "1": "UNREAD EMAILS",
    "2": "EMAILS FROM THE LAST DAY (TODAY)",
    "3": "THE LAST ONE RECEIVED",
    "4": "ALL EMAILS",
}

def select_and_fetch_data() -> List[Dict[str, Any]]:
    """Prompts user for data source and returns the email list."""
    
    print("\n--- Data Source Selection ---")
    print("1: Use Local Mock File (email_data.py)")
    print("2: Connect to Live Gmail Account (Requires App Password)")
    
    source_choice = input("Enter data source choice (1 or 2): ")
    
    if source_choice == "1":
        print("Using local mock file...")
        return EMAILS # Return the list imported from the local file
    
    elif source_choice == "2":
        print("\n--- Gmail Authentication ---")
        print("NOTE: You need an App Password (not your regular password).")
        
        GMAIL_USERNAME = input("Enter Gmail Username (e.g., yourname@gmail.com): ")
        GMAIL_APP_PASSWORD = input("Enter Gmail App Password: ")
        
        fetcher = GmailFetcher(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
        return fetcher.connect_and_fetch(count=10) # Fetch up to 10 live emails
    
    else:
        print("Invalid source choice. Defaulting to local file.")
        return EMAILS


def run_email_processor():
    """Manages the program loop and user interaction."""
    
    # STEP 1: SELECT AND FETCH DATA
    email_data = select_and_fetch_data()
    
    if not email_data:
        print("\nFATAL ERROR: Could not load any email data. Exiting.")
        return

    # STEP 2: LOCAL INITIALIZATION
    mailbox = Mailbox(email_data)
    reporter = ReportGenerator()
    print(f"Data Source Initialized with {len(email_data)} emails.")
    
    # STEP 3: MAIN LOOP
    while True:
        # Display the main filtering menu
        print("\n" + "=" * 50)
        print("EMAIL FILTERING CHOICES:")
        for key, title in FILTER_TITLES.items():
            print(f"{key}: View {title}")
        print("0: Exit Program")
        print("=" * 50)
        
        choice = input("Enter your filter choice (1, 2, 3, 4, or 0): ")
        
        if choice == "0":
            print("Exiting the program. Goodbye! 👋")
            break
        
        handler_func = FILTER_FUNCTIONS.get(choice)

        if handler_func:
            filtered_emails = handler_func(mailbox)
            title = FILTER_TITLES.get(choice) 

            # Output Choice Prompt
            print("\n--- Output Destination ---")
            print("1: Print to Terminal")
            print("2: Export to JSON File")
            print("3: Export to TXT File")
            print("4: Export to CSV File") 
            output_choice = input("Enter output choice (1, 2, 3, or 4): ")

            # Dispatch: Call the factory method
            reporter.dispatch_report(filtered_emails, title, output_choice)
            
            input("\nPress Enter to see the filter choices again...")
            
        else:
            # Invalid Filter Choice Handler
            print("Invalid filter choice. Please enter a number from the list.")
            continue


if __name__ == "__main__":
    run_email_processor()
