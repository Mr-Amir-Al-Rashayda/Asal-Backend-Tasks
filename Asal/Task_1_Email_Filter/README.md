# 📨 Asal Technologies - Backend Training Task 1: Basic Email Filter

## Project Goal
This project's primary goal was to **practice foundational Python concepts** essential for backend development, specifically **Control Flow** and **Data Filtering**, by simulating the process of managing an inbox.

---
### Key Principles Applied:
* **Modularity & Organization:** The code logic and data are conceptually separate (imported from `email_data.py`).
* **Clean Code:** The code adheres to professional naming conventions (e.g., concise variable names).
* **Efficiency:** The core filtering logic (though currently in simple functions) is designed to be easily upgraded to efficient **List Comprehensions**.
* **Safety:** The **Defensive Programming** principle is applied to protect the original data source.

### 1. File Structure (Original)
* **`classifier`**: Contains all the functional logic, including the filtering functions, printing mechanism, and the main user interaction loop. (This file would ideally be split into `mailbox.py`, `report_generator.py`, and `main.py`).
* **`email_data.py`**: Serves as the mock data source. It holds the list of email dictionaries, simulating a database or API response with fields like `status` and `days_ago`.
* **`AsalTask1.drawio`**: The raw diagram file for the project's control flow.

---

### 2. Control Flow Logic (The Decision Block)

The program runs inside a continuous `while True` loop, where the user's choice is processed through sequential decision logic. (This is ready to be refactored into a **Dictionary Dispatch Table**).

| User Choice | Description | Action & Loop Control |
| :--- | :--- | :--- |
| **'1'** | **UNREAD Emails** | Calls `filter_unread_emails()`. **Continues loop.** |
| **'2'** | **LAST DAY Emails** | Calls `filter_last_day_emails()`. **Continues loop.** |
| **'3'** | **LAST ONE Email** | Calls `filter_last_one()`. **Continues loop.** |
| **'4'** | **ALL Emails** | Calls `filter_all_emails()`. **Continues loop.** |
| **'0'** | **EXIT Program** | Executes **`break`** to exit the application loop. |
| *Other Input* | **Invalid Input** | Executes **`continue`** to restart the menu prompt. |

---

### 3. Flow Chart Overview
The **flow chart** illustrates the step-by-step evaluation of user input, ensuring that only one filtering function is executed per valid choice.
It highlights the proper use of:
* **Sequential decision-making**
* **Loop control** (`break` and `continue`)
* **Input validation**

---

## How to Run

1.  Ensure both `classifier` and `email_data.py` are in the **same folder**.
2.  Open your **Terminal / Command Prompt** in that folder.
3.  Run the following command:

    ```bash
    python main.py
    ```
```eof
