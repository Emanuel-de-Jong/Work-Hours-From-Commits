import re
import os
from datetime import datetime, timedelta

TIME_FORMAT = "%H:%M"

def get_input_file():
    for f in os.listdir():
        if f.lower().endswith(".yml"):
            return f
    raise FileNotFoundError("No .yml file found in current directory")

def parse_time(t):
    return datetime.strptime(t, TIME_FORMAT)

def format_duration(start, end):
    start_dt = parse_time(start)
    end_dt = parse_time(end)
    if end_dt < start_dt:
        end_dt += timedelta(days=1)
    diff = (end_dt - start_dt).seconds
    hours = diff // 3600
    minutes = (diff % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

def update_total_times(lines):
    updated = []
    group = []
    for line in lines + [""]:
        if line.strip().startswith("- ") and group:
            updated += process_group(group)
            group = []
        group.append(line)
    if group:
        updated += process_group(group)
    return updated[:-1] if updated[-1] == "" else updated

def process_group(group_lines):
    start_time = None
    end_time = None
    total_index = None
    for idx, line in enumerate(group_lines):
        if "start_time:" in line:
            match = re.search(r"start_time:\s*'?(?P<val>\d{1,2}:\d{2})'?", line)
            if match:
                start_time = match.group("val")
        if "end_time:" in line:
            match = re.search(r"end_time:\s*'?(?P<val>\d{1,2}:\d{2})'?", line)
            if match:
                end_time = match.group("val")
        if "total_time:" in line and total_index is None:
            total_index = idx
    if start_time and end_time and total_index is not None:
        duration = format_duration(start_time, end_time)
        indent = re.match(r"^(\s*)", group_lines[total_index]).group(1)
        group_lines[total_index] = f"{indent}total_time: '{duration}'"
    return group_lines

def main():
    input_file = get_input_file()
    with open(input_file, "r") as f:
        lines = f.read().splitlines()
    updated_lines = update_total_times(lines)
    with open(input_file, "w") as f:
        f.write("\n".join(updated_lines))

if __name__ == "__main__":
    main()
