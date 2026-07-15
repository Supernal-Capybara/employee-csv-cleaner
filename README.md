# Employee CSV Cleaner & Reporting Tool

This is a Python tool that:

* Reads employee data from a CSV file
* Cleans inconsistent formatting (whitespace, department names, capitalization)
* Validates rows for missing or invalid data
* Skips invalid records safely
* Writes a cleaned CSV output file
* Generates a console report with:

  * total rows processed
  * valid vs invalid rows
  * total hours worked
  * average hours worked
  * average pay rate
  * total payroll cost estimate
  * employee count by department
  * displays the top five earners based on total earnings

This project was built as a practical internal-tool style Python script similar to the kinds of small automation and reporting utilities used in offices, hospitals, schools, and business IT departments.


# Notes
Main file: `csv_cleanup_report.py`
Helper file: `generate_test_data_for_csv_tool.py`
Test file: `test_csv_cleanup_report.py`

This project also includes an optional helper file that helps to generate test CSV data as well as a test file.  
All three files should be kept in the same folder when running the program.


# Testing
Install dependencies and run the test file `test_csv_cleanup_report.py`

* In PowerShell:
  * py -m pip install pytest
  * py -m pytest