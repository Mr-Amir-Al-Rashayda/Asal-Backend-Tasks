import json
from .writer_base import BaseWriter, EmailDict

class JsonWriter(BaseWriter):
    """Writes the report to a JSON file."""
    def write_report(self):
        file_name = f"{self.title.replace(' ', '_').lower()}_report.json"
        
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(self.emails, f, ensure_ascii=False, indent=4)
            print(f"SUCCESS: Report saved to JSON file: {file_name}")
        except IOError:
            print(f"ERROR: Could not write to file {file_name}.")
