#  Asal Technologies - Backend Training Task 1: Basic Email Filter

##  Project Goal
This project's primary goal was to **practice foundational Python concepts** essential for backend development, specifically **Control Flow** and **Data Filtering**, by simulating the process of managing an inbox.
---

##  Implementation Details

### 1. File Structure
- **`classifier.py`**: Contains all the functional logic, including the filtering functions, printing mechanism, and the main user interaction loop.  
- **`email_data.py`**: Serves as the mock data source. It holds the list of email dictionaries, simulating a database or API response with fields like `status` and `days_ago`.  
- **`AsalTask1.drawio`**: The raw diagram file for the project's control flow.  
---

### 2. Control Flow Logic (The Decision Block)
The program runs inside a continuous `while True` loop, controlled by the user's input.  
The sequential decision logic is as follows:

| User Choice | Description | Logic |
|--------------|--------------|--------|
| `'1'` | **UNREAD Emails** | Checked first using `if choice == "1"`. Calls `filter_unread_emails()`. Continues loop. |
| `'2'` | **LAST DAY Emails** | Checked next using `elif choice == "2"`. Calls `filter_last_day_emails()`. Continues loop. |
| `'3'` | **LAST ONE Email** | Checked next using `elif choice == "3"`. Calls `filter_last_one()`. Continues loop. |
| `'4'` | **ALL Emails** | Checked next using `elif choice == "4"`. Calls `filter_all_emails()`. Continues loop. |
| `'0'` | **EXIT Program** | Checked using `elif choice == "0"`. Executes `break` to exit the loop. |
| *Other Input* | **Invalid Input** | Handled by `else`. Executes `continue` to restart the loop. |

---

### 3. Flow Chart Overview
The **flow chart** illustrates the step-by-step evaluation of user input, ensuring that only one filtering function is executed per valid choice.  
It highlights the proper use of:
- **Sequential decision-making**
- **Loop control**
- **Input validation**

---

## 🚀 How to Run

1. Ensure both `classifier.py` and `email_data.py` are in the **same folder**.
2. Open your **Terminal / Command Prompt** in that folder.
3. Run the following command:

   ```bash
   python classifier.py
