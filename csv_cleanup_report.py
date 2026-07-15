
import csv
import generate_test_data_for_csv_tool

from pathlib import Path

BASE_DIR = Path(__file__).parent

original_file = BASE_DIR / "arasaka_employees.csv"
cleaned_file = BASE_DIR / "arasaka_employees_final.csv"



header = ["name", "department", "hours_worked", "pay_rate"]

test_rows = [
    ["Alice Johnson", "Sales", "40", "20.50"],
    [" Bob Smith ", "sales", "38.5", "19.75"],
    ["Cara Nguyen", " HR ", "41", "24.00"],
    ["Daniel Reed", "IT", "40", "27.25"],
    ["Elena Park", "Finance", "37.5", "26.10"],
    ["Greta Bergman", "Operations", "42", "21.40"],
    ["George Brown", "Sales", "39", "20.00"],
    ["Hannah Lee", "HR", "40", "23.50"],
    ["Isaac King", "IT", "36.5", "28.00"],
    ["Julia Chen", "Finance", "40", "25.75"],

    # Messy but salvageable rows
    [" Kevin Diaz ", " operations ", " 40 ", " 22.00 "],
    ["Laura Moss", "SALES", "35", "18.90"],
    ["Mike O'Brien", " it ", "40.0", "29.10"],
    ["Nina Patel", "Hr", "39.5", "24.25"],

    # Invalid rows
    ["", "Sales", "40", "20.50"],              # missing name
    ["Oscar Hill", "", "40", "20.50"],         # missing department
    ["Priya Shah", "Finance", "abc", "25.00"], # bad hours
    ["Quentin Ray", "IT", "-5", "30.00"],      # negative hours
    ["Rosa Diaz", "HR", "40", "invalid"],      # bad pay
    ["Sam Cole", "Sales", "40", "-10"],        # negative pay

    # More realistic mixed rows
    ["Tara Brooks", "Customer Support", "40", "18.50"],
    ["Uma Flores", "customer support", "39", "18.75"],
    ["Victor Lane", "Warehouse", "44", "17.20"],
    ["Wendy Cho", "Warehouse ", "43.5", "17.20"],
    ["Xavier Price", "Procurement", "40", "23.10"],
    ["Ekaterina Kostova", "procurement", "38", "22.95"],
    ["Zane Miller", "Logistics", "41", "21.80"],
]

def read_csv(path):
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            invalid_rows = 0
            valid_rows = 0
            
            data = []
            rows = csv.reader(f)
            
            header = next(rows)
            
            for row in rows:
                cleaned_row = clean_row(row)
                if cleaned_row is None:
                    invalid_rows += 1
                    continue
                
                validated_row = validate_row(cleaned_row)
                if validated_row is None:
                    invalid_rows += 1
                    continue
    
                valid_rows += 1
                data.append(validated_row)
                
            return header, data, invalid_rows, valid_rows
        
    except OSError as e:
        print(f"Could not read file: {e}")
        return None

# name, department, hours_worked, pay_rate
def clean_row(row):
    if len(row) != 4:
        return None
    
    name, department, hours_worked, pay_rate = [item.strip() for item in row]

    return name, department.upper(), hours_worked, pay_rate


def validate_row(cleaned_row):
    if cleaned_row is None:
        return None
    
    name, department, hours_worked, pay_rate = cleaned_row
    
    if not name or not department:
        return None
    
    try:
        hours_worked = float(hours_worked)
    except ValueError:
        return None

    if hours_worked < 0:
        return None
    
    try:
        pay_rate = float(pay_rate)
    except ValueError:
        return None
    
    if pay_rate <= 0:
        return None
    
    validated_row = (name, department, hours_worked, pay_rate)
    return validated_row

def write_clean_csv(path, cleaned_rows, header):
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(cleaned_rows)
            print(f"File saved at: {path}")
            
    except OSError as e:
        print(f"Could not write file: {e}")
        return None

def print_report(data, invalid_rows, valid_rows):
    total_hours = 0
    count = 0
    total_pay = 0
    dept_personnel_tracker = {}
    total_payroll = 0
    
    print("\nData report: ")
    print(f"Total rows read: {invalid_rows + valid_rows}")
    print(f"Valid rows: {valid_rows}")
    print(f"Invalid rows: {invalid_rows}")
    
    for _, department, hours_worked, pay_rate in data:
        total_hours += hours_worked
        total_pay += pay_rate
        total_payroll += hours_worked * pay_rate
        count += 1
        dept_personnel_tracker[department] = dept_personnel_tracker.get(department, 0) + 1
    
    print(f"\nTotal hours worked: {total_hours:.2f}")

    
    if count > 0:
        print(f"Average hours worked: {total_hours / count:.2f}")
        print(f"Average pay rate: ${total_pay / count:.2f}")
    else:
        print("No payrate or average hours worked data available.")

    print(f"Total payroll cost estimate: ${total_payroll:.2f}")
    
    print("Employee count by department: ")
    print(", ".join(f"{k}: {v}" for k, v in sorted(dept_personnel_tracker.items())))
    
    print("\nCleaned employee data: ")
    print(f"{'Name':<20} {'Dept':<16} {'Hours':>8} {'Pay':>7}")
    print("-" * 56)
    
    sorted_data = sorted(data, key=lambda row: (row[1], -row[3]))
    
    for name, dept, hrs, pay in sorted_data:
        print(f"{name:<20} {dept:<16} {hrs:>8.1f} {pay:>8.2f}")
        
    print("\nTop five earners:")
    print(f"{'Name':<20} {'Dept':<16} {'Hours':>8} {'Pay':>7} {'Total':>10}")
    print("-" * 67)
    sorted_earners =sorted(data, key=lambda row: row[2] * row[3], reverse=True)
    for name, dept, hrs, pay in sorted_earners[:5]:
        total = hrs * pay
        print(f"{name:<20} {dept:<16} {hrs:>8.1f} {pay:>8.2f} {total:>10.2f}")
    
    
if __name__ == "__main__":
    GENERATE_TEST_DATA = True

    if GENERATE_TEST_DATA:
        generate_test_data_for_csv_tool.write_test_csv(original_file, header, test_rows)
    
    header, data, invalid_rows, valid_rows = read_csv(original_file)
    write_clean_csv(cleaned_file, data, header)
    print_report(data, invalid_rows, valid_rows)

 