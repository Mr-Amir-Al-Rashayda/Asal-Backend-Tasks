from typing import List, Dict, Any
from output_strategy import TerminalWriter, JsonWriter, TxtWriter, CsvWriter 

EmailDict = Dict[str, Any]

class ReportGenerator:
    """
    Acts as the factory for output writers. It routes the data without knowing
    how the specific file formats are handled (adhering to OCP).
    """

    # Maps choice to the specific Writer Class
    WRITER_CLASSES = {
        "1": TerminalWriter,
        "2": JsonWriter,
        "3": TxtWriter,
        "4": CsvWriter, 
    }

    def dispatch_report(self, filtered_emails: List[EmailDict], title: str, output_choice: str):
        """
        Routes the filtered data to the correct Writer object based on user choice.
        """
        
        WriterClass = self.WRITER_CLASSES.get(output_choice)

        print("\n" + "=" * 80)
        print(f"REPORT PREPARATION: {title}")
        print("=" * 80)

        if WriterClass:
            # 1. Instantiation: Create the writer object
            writer_instance = WriterClass(filtered_emails, title)
            
            # 2. Execution: Call the standard method (write_report)
            writer_instance.write_report()
        else:
            print("ERROR: Invalid output choice. Data was not exported.")