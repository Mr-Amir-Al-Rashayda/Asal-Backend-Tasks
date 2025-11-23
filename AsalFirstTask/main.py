
from mailbox import Mailbox
from report_generator import ReportGenerator 
from data_loaders import LocalFileLoader, GmailLoader, EmailLoader, DatabaseLoader # MODIFIED
from typing import List, Dict, Any, Optional # Add Optional 


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

def create_data_loader() -> Optional[EmailLoader]: # Renamed function
    """
    Factory function: Prompts user for data source and returns the 
    correct concrete EmailLoader object.
    """
    
    print("\n--- Data Source Selection ---")
    print("1: Use Local Mock File (email_data.py)")
    print("2: Connect to Live Gmail Account (Requires App Password)")
    print("3: Load from MySQL Database") 
    
    source_choice = input("Enter data source choice (1, 2, or 3): ")
    
    # Dispatch dictionary for cleaner code
    def create_local_loader():
        return LocalFileLoader()
    
    def create_gmail_loader():
        print("\n--- Gmail Authentication ---")
        print("NOTE: You need an App Password (not your regular password).")
        
        GMAIL_USERNAME = input("Enter Gmail Username (e.g., yourname@gmail.com): ")
        GMAIL_APP_PASSWORD = input("Enter Gmail App Password: ")
        
        return GmailLoader(GMAIL_USERNAME, GMAIL_APP_PASSWORD, count=10)
    
    def create_database_loader():
        return DatabaseLoader()
    
    # Dispatch dictionary mapping choices to factory functions
    LOADER_FACTORIES = {
        "1": create_local_loader,
        "2": create_gmail_loader,
        "3": create_database_loader,
    }
    
    factory_func = LOADER_FACTORIES.get(source_choice)
    if factory_func:
        return factory_func()
    else:
        print("Invalid source choice.")
        return None
    

def run_email_processor():
    """Manages the program loop and user interaction."""
    
    # --- STEP 1: SELECT LOADER (Factory) ---
    loader = create_data_loader() # Get the loader *strategy*
    
    if not loader:
        print("\nFATAL ERROR: No data loader selected. Exiting.")
        return

    # --- STEP 2: FETCH DATA (Execute Strategy) ---
    # The abstraction in action!
    # main.py does not know if this is loading from a file or Gmail.
    email_data = loader.load_emails()
    
    if not email_data:
        print("\nFATAL ERROR: Could not load any email data. Exiting.")
        return

    # --- STEP 3: LOCAL INITIALIZATION (Unchanged) ---
    mailbox = Mailbox(email_data)
    reporter = ReportGenerator()
    print(f"Data Source Initialized with {len(email_data)} emails.")
    
    # --- STEP 4: MAIN LOOP ---
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