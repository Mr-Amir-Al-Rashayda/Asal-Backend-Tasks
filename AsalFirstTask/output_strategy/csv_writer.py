import csv
from .writer_base import BaseWriter

class CsvWriter(BaseWriter):
    """Writes the report to a CSV file."""
    def write_report(self):
        file_name = f"{self.title.replace(' ', '_').lower()}_report.csv"
        
        fieldnames = ['id', 'sender', 'subject', 'status', 'days_ago', 'body_snippet']
        
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                
                writer.writeheader()
                writer.writerows(self.emails)
                
            print(f"SUCCESS: Report saved to CSV file: {file_name}")
        except IOError:
            print(f"ERROR: Could not write to file {file_name}.")
