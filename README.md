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


