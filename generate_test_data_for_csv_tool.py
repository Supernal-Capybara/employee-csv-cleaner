
import csv

def write_test_csv(path, header, rows):
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"Test CSV created at: {path}")
        
    except OSError as e:
        print(f"Could not write file: {e}")
        
