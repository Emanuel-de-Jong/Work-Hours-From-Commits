import yaml
import csv
import os

DEFAULT_TITLE = "Various changes"

def get_input_file():
    for f in os.listdir():
        if f.lower().endswith(".yml"):
            return f
    raise FileNotFoundError("No .yml file found in current directory")

def load_groups(input_file):
    with open(input_file, "r") as f:
        return yaml.safe_load(f) or []

def write_csv(groups, input_file):
    output_file = input_file.replace(".yml", ".csv")
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["start", "end", "date", "duration", "description"])
        for group in groups:
            title = group.get("title") or DEFAULT_TITLE
            row = [
                group.get("start_time", ""),
                group.get("end_time", ""),
                group.get("date", ""),
                group.get("total_time", ""),
                title
            ]
            writer.writerow(row)

def main():
    input_file = get_input_file()
    groups = load_groups(input_file)
    write_csv(groups, input_file)

if __name__ == "__main__":
    main()
