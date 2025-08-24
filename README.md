# Work Hours From Commits
Estimate the hours that you worked on a project using the commits in your git repo(s). It looks at the times between commits and groups time blocks together. The end result is a neat CSV with task descriptions from the commit messages and next to them the total time they took.

Of course these are just guesses and can't replace manual hour tracking. But it's better than nothing if you forgot to track them.

**Active Development:** <br>
**Last Change:** <br>

| | |
| :---: | :---: |
| ![](/Screenshots/1-Output-YML.png) | ![](/Screenshots/2-Output-CSV.png) |

## Usage
1. Put correct repo paths and links in `script_1.py`. Optionally tweak other params.
2. Run `script_1.py`.
3. In `groups.yml`, remove unwanted groups, change start times if total time is unrealistic, change titles.
4. Run `script_2.py`.
5. The new `hours.csv` are your hours by task.
