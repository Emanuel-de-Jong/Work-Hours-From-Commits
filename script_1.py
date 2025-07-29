import subprocess
import datetime
import random
import yaml

REPOS = {
    "https://github.com/Emanuel-de-Jong/Gosuji": "D:\\Coding\\Repos\\Gosuji",
    "https://github.com/Emanuel-de-Jong/Gosuji-TEMP": "D:\\Coding\\Repos\\Gosuji-TEMP"
}

START_DATE = "2024-07-05"
END_DATE = "2025-12-01"
MAX_GAP_HOURS = 2.0
BASE_OFFSET_MINUTES = 30
VARIANCE_MINUTES = 5

def load_commits():
    all_commits = []
    for base_url, repo_path in REPOS.items():
        fmt = "%H%x1f%ad%x1f%s%x1f%b"
        cmd = ["git", "-C", repo_path, "log", f"--pretty=format:{fmt}", "--date=iso-strict"]
        out = subprocess.check_output(cmd, text=True)

        for line in out.splitlines():
            parts = line.split("\x1f")
            if len(parts) < 4:
                continue
            sha, datestr, subject, body = parts[0], parts[1], parts[2], parts[3]
            dt = datetime.datetime.fromisoformat(datestr.strip())
            all_commits.append((dt, sha, subject.strip(), body.strip(), base_url))

    if not all_commits:
        return []

    tzinfo = all_commits[0][0].tzinfo
    start_dt = datetime.datetime.fromisoformat(START_DATE).replace(tzinfo=tzinfo)
    end_dt = (datetime.datetime.fromisoformat(END_DATE) + datetime.timedelta(days=1)).replace(tzinfo=tzinfo)

    all_commits = [c for c in all_commits if start_dt <= c[0] < end_dt]
    all_commits.sort(key=lambda x: x[0])
    return all_commits

def group_commits(commits):
    groups = []
    if not commits:
        return groups

    current_group = [commits[0]]
    for commit in commits[1:]:
        prev_dt = current_group[-1][0]
        if (commit[0] - prev_dt).total_seconds() <= MAX_GAP_HOURS * 3600:
            current_group.append(commit)
        else:
            groups.append(current_group)
            current_group = [commit]
    groups.append(current_group)
    return groups

def format_duration(td):
    total_minutes = int(td.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"

def build_group_dict(group):
    first_dt, first_sha, first_subject, first_body, _ = group[0]
    last_dt = group[-1][0]

    date_str = first_dt.date().isoformat()
    random_variation = random.randint(0, VARIANCE_MINUTES)
    start_time = first_dt - datetime.timedelta(minutes=BASE_OFFSET_MINUTES + random_variation)
    end_time = last_dt

    start_time = start_time.replace(second=0)
    end_time = end_time.replace(second=0)
    total_time = format_duration(end_time - start_time)

    commits_data = {}
    per_repo = {}
    for dt, sha, subject, body, base_url in group:
        short_sha = sha[:8]
        message = f"{subject} {body}".strip()
        message = " ".join(message.split())
        url = f"{base_url}/commit/{short_sha}"
        commits_data[url] = message
        if base_url not in per_repo:
            per_repo[base_url] = []
        per_repo[base_url].append(short_sha)

    combined_changes = []
    for base_url, shas in per_repo.items():
        if len(shas) > 1:
            combined_changes.append(f"{base_url}/compare/{shas[0]}...{shas[-1]}")
        else:
            combined_changes.append(f"{base_url}/commit/{shas[0]}")

    title = ""
    for _, _, subject, body, _ in group:
        combined = f"{subject} {body}".strip()
        if len(combined) > 1:
            title = combined
            break

    return {
        "title": title,
        "total_time": total_time,
        "date": date_str,
        "start_time": start_time.strftime("%H:%M"),
        "end_time": end_time.strftime("%H:%M"),
        "combined_changes": combined_changes,
        "commits": commits_data
    }

def main():
    commits = load_commits()
    grouped = group_commits(commits)
    data = [build_group_dict(group) for group in grouped]

    raw_yaml = yaml.safe_dump(data, sort_keys=False, width=float("inf"))
    lines = raw_yaml.splitlines()
    spaced_lines = []
    for i, line in enumerate(lines):
        if i > 0 and line.startswith("- "):
            spaced_lines.append("")
        spaced_lines.append(line)

    output_file_name = f"{START_DATE}_{END_DATE}.yml"
    with open(output_file_name, "w") as f:
        f.write("\n".join(spaced_lines))

if __name__ == "__main__":
    main()
