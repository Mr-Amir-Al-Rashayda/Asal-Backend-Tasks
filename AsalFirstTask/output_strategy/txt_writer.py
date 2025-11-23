from .writer_base import BaseWriter

class TxtWriter(BaseWriter):
    """Writes the full report to a plain TXT file."""
    def write_report(self):
        file_name = f"{self.title.replace(' ', '_').lower()}_report.txt"
        
        report_lines = []
        report_lines.append(f"REPORT: {self.title} | Total Emails: {len(self.emails)}\n")
        report_lines.append("--------------------------------------------------------------------------------\n")
        report_lines.append("ID | Sender | Subject | Body Snippet\n")
        report_lines.append("--------------------------------------------------------------------------------\n")
        
        for mail in self.emails:
            # Full content without limits for file export
            report_lines.append(f"{mail.get('id')} | {mail.get('sender')} | {mail.get('subject')} | {mail.get('body_snippet')}\n")
            
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.writelines(report_lines)
            print(f"SUCCESS: Report saved to TXT file: {file_name}")
        except IOError:
            print(f"ERROR: Could not write to file {file_name}.")
