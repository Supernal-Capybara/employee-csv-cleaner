
from csv_cleanup_report import clean_row, validate_row, read_csv, write_clean_csv, print_report
import csv
import pytest

def test_clean_row_strips_whitespace_and_uppercases_department():
    row = [" Bob Smith ", " sales ", "38.5", "19.75"]

    result = clean_row(row)

    assert result == ("Bob Smith", "SALES", "38.5", "19.75")
    
    
def test_clean_row_rejects_wrong_number_of_fields():
    row = ["Alice Johnson", "Sales", "40"]

    result = clean_row(row)

    assert result is None
    
def test_validate_row_converts_numbers_to_floats():
    cleaned_row = ("Alice Johnson", "SALES", "40", "20.50")

    result = validate_row(cleaned_row)

    assert result == ("Alice Johnson", "SALES", 40.0, 20.5)
    
    
def test_validate_row_rejects_nonnumeric_hours():
    row = ("Emily Johannson", "FINANCE", "abc", "25.00")
    
    result = validate_row(row)
    
    assert result is None
    
    
def test_validate_row_rejects_negative_hours():
    row = ("Anders Helmann", "Engineering", "-5", "30.00")
    
    result = validate_row(row)
    
    assert result is None
    

@pytest.mark.parametrize(
    "pay_rate",
    ["invalid", "0", "-5"],
)
def test_validate_row_rejects_invalid_pay_rate(pay_rate):
    row = ("Panam Palmer", "TRANSPORTATION", "40", pay_rate)

    result = validate_row(row)

    assert result is None


def test_read_csv_reads_valid_row(tmp_path):
    test_file = tmp_path / "employees.csv"

    test_file.write_text(
        "name,department,hours_worked,pay_rate\n"
        "Yorinobu Arasaka,Sales,40,20.50\n",
        encoding="utf-8"
    )

    header, data, invalid_rows, valid_rows = read_csv(test_file)

    assert header == ["name", "department", "hours_worked", "pay_rate"]
    assert data == [("Yorinobu Arasaka", "SALES", 40.0, 20.5)]
    assert invalid_rows == 0
    assert valid_rows == 1
    
    
def test_read_csv_skips_invalid_rows(tmp_path):
    test_file = tmp_path / "employees.csv"
    
    test_file.write_text(
        "name,department,hours_worked,pay_rate\n"
        "Alice Johnson,Sales,40,20.50\n"
        "Priya Shah,Finance,abc,25.00\n",
        encoding="utf-8"
    )
    
    header, data, invalid_rows, valid_rows = read_csv(test_file)
    
    assert data == [("Alice Johnson","SALES",40.0,20.50)]
    assert invalid_rows == 1
    assert valid_rows == 1


def test_write_clean_csv_writes_header_and_rows(tmp_path):
    output_file = tmp_path / "cleaned_employees.csv"

    header = ["name", "department", "hours_worked", "pay_rate"]

    cleaned_rows = [
        ("Alice Johnson", "SALES", 40.0, 20.5),
        ("Daniel Reed", "IT", 38.0, 27.25),
    ]
    
    write_clean_csv(output_file, cleaned_rows, header)
    
    with open(output_file, "r", encoding="utf-8", newline="") as file:
        rows = list(csv.reader(file))
        
        assert rows[0] == header
        assert rows[1] == ["Alice Johnson", "SALES", "40.0", "20.5"]
        assert rows[2] == ["Daniel Reed", "IT", "38.0", "27.25"]
        
        

def test_print_report_displays_summary(capsys):
    data = [
        ("Alice Johnson", "SALES", 40.0, 20.5),
    ]

    print_report(data, invalid_rows=1, valid_rows=1)

    captured = capsys.readouterr()
    output = captured.out

    assert "Total rows read: 2" in output
    assert "Valid rows: 1" in output
    assert "Invalid rows: 1" in output
    assert "Total payroll cost estimate: $820.00" in output
    


def test_print_report_handles_empty_data(capsys):
    data = []

    print_report(data, invalid_rows=2, valid_rows=0)

    captured = capsys.readouterr()
    output = captured.out

    assert "Total rows read: 2" in output
    assert "Valid rows: 0" in output
    assert "No payrate or average hours worked data available." in output
    assert "Total payroll cost estimate: $0.00" in output
    


def test_read_csv_handles_missing_file(tmp_path, capsys):
    missing_file = tmp_path / "missing.csv"

    result = read_csv(missing_file)

    captured = capsys.readouterr()

    assert result is None
    assert "Could not read file:" in captured.out
    
    
