# classifier.py
from email_data import EMAILS

# 1. Filter function (The User's Choices)
def filter_unread_emails(emails_list):
    """Returns a list of emails that are UNREAD."""
    unread_list = []
    for email in emails_list:
        if email.get('status') == "UNREAD": 
            unread_list.append(email)
    return unread_list

def filter_last_day_emails(emails_list):
    """Returns a list of emails received today (0 days ago)."""
    today_list = []
    for email in emails_list:
        if email.get('days_ago') == 0: 
            today_list.append(email)
    return today_list

def filter_last_one(emails_list):
    """Returns a list containing only the most recent email."""
    if emails_list:
        return [emails_list[-1]] 
    return []

def filter_all_emails(emails_list):
    """Returns all emails (The default choice)."""
    return emails_list

# 2. Printing function (Output the results)
def process_and_print_emails(emails_list):
    """
    Loops through the filtered list and prints basic email information.
    """
    if not emails_list:
        print("No emails found for this choice.")
        return

    # Print a header for the output table
    print("ID    | Sender (First 25 chars)   | Subject (First 40 chars) ")
    print("--------------------------------------------------------------------------------")
    for mail in emails_list:
        # Get the values, using a simple default if the key is missing (mail.get)
        mail_id = mail.get('id', 'N/A')
        sender = mail.get('sender', 'N/A')
        subject = mail.get('subject', 'No Subject')
                
        print(str(mail_id) + " | " + sender[:25] + " | " + subject[:40])

# 3. Main flow (Handles User Input)
def run_email_processor(emails_list):
    """
    Presents choices to the user, takes input, and runs the corresponding filter.
    """
    while True:
        print("\n" + "=" * 50)
        print("EMAIL FILTERING CHOICES:")
        print("1: View UNREAD Emails")
        print("2: View Emails from the LAST DAY (Today)")
        print("3: View the LAST ONE (Most Recent) Email")
        print("4: View ALL Emails")
        print("0: Exit Program")
        print("=" * 50)
        
        choice = input("Enter your choice (1, 2, 3, 4, or 0): ")
        
        if choice == "1":
            filtered_emails = filter_unread_emails(emails_list)
            title = "UNREAD EMAILS"
        elif choice == "2":
            filtered_emails = filter_last_day_emails(emails_list)
            title = "EMAILS FROM THE LAST DAY (TODAY)"
        elif choice == "3":
            filtered_emails = filter_last_one(emails_list)
            title = "THE LAST ONE RECEIVED"
        elif choice == "4":
            filtered_emails = filter_all_emails(emails_list)
            title = "ALL EMAILS"
        elif choice == "0":
            print("Exiting the program. Goodbye!")
            break 
        else:
            print("Invalid choice. Please enter a number from the list.")
            continue 


        print("\n" + "-" * 80)
        print(f"REPORT FOR: {title}")
        print(f"Total emails found: {len(filtered_emails)}")
        print("-" * 80)

        process_and_print_emails(filtered_emails)
        
        input("\nPress Enter to see the choices again...")


if __name__ == "__main__":
    run_email_processor(EMAILS)


# Initial commit: Added Asal Task 1 folder and classifier.py
