# CSA08-192365059-Assignment3

**Assignment:** Assignment 3 – List, Set, Tuple, Dictionary  
**Course:** CSA08 – Python Programming  
**Student:** Karthikeyan S  
**Register Number:** 192365059  
**Nature:** Individual  
**Platform:** Windows 10  
**Python command:** `python`  
**Python version:** Python 3.11.6

**GitHub repository:** https://github.com/Karthikdj2028/CSA08-192365059-Assignment3

## Project overview

This assignment covers all seven questions using beginner-friendly Python: lists and slicing, tuples, aliasing and copying, dictionaries, sets, list comprehensions, nested data, and a contact-merging design. No classes or third-party packages are required.

| Folder | Question | Main work |
|---|---|---|
| Task01 | Q1 – Lists and Slicing: Daily Rainfall Records | Weekly totals, extremes, dry days, moving average and benchmarks |
| Task02 | Q2 – Tuples, Mutability and Copying | Tuple dictionary keys, grid aliasing, shallow/deep copies and memory/time checks |
| Task03 | Q3 – Dictionaries: Farmer Helpline Complaint Analysis | Word counts, district grouping, top-k words and dictionary/Counter/list.count benchmarks |
| Task04 | Q4 – Sets: Elective Registration Clash Detection | Set operations, Venn diagram, membership and intersection benchmarks |
| Task05 | Q5 – List Comprehension: Cleaning Sensor Readings | Loop, comprehension, map/filter/lambda, alarms, time and memory |
| Task06 | Q6 – Nested Data: A Railway Timetable | Five-train nested structure, station index, query benchmarks and memory |
| Task07 | Q7 – Design a Contact-Merging Program from First Principles | Normalisation, dictionary indexes, duplicate merging and pairwise comparison |

Each task folder contains the Python source, a short analysis/answer file, a task README and an `evidence/` directory. Benchmark programs write their raw measurements to CSV files in their task folders.

## Python and libraries

- Python 3.11.6 on Windows 10, run with `python`.
- Third-party packages: none.
- Standard-library modules used: `random`, `time`, `sys`, `copy`, `collections`, `string`, `csv`, `itertools`, `tracemalloc` and `statistics`.
- `requirements.txt` is included. No `pip install` is needed.

## Setup on Windows

Open the inner `CSA08-192365059-Assignment3` folder in VS Code. Select **Terminal → New Terminal**. Confirm the terminal is in the folder containing this README.

```powershell
python --version
git --version
pwd
```

Expected Python version: `Python 3.11.6`.

### Run with F5 in VS Code

The project includes `.vscode/launch.json`. Open any `.py` file inside this workspace and press **F5**. Choose **Python Debugger** if VS Code asks. The program runs in the integrated terminal with the project root as its working directory. You can also use the commands below.

## Run commands

Run these commands from the project root:

| Task | Command | What to check |
|---|---|---|
| Task01 | `python Task01/rainfall.py` | 365 daily readings, weekly totals, wettest/driest week, maximum/minimum day, 7-day averages, dry days, edge cases and timing for 365 / 36,500 / 365,000 days. Writes `Task01/rainfall_benchmark.csv`. |
| Task02 | `python Task02/tuples_copying.py` | Bad/good grid, `is()` and `id()`, tuple dictionary keys, shallow/deep copy, tuple containing a list, million-item memory and timing. |
| Task03 | `python Task03/complaints.py` | `get()`, `setdefault()`, stop words, top-k ordering, district groups, empty/punctuation cases and 1,000 / 10,000 / 100,000 complaint benchmark. Writes `Task03/complaints_benchmark.csv`. |
| Task04 | `python Task04/electives.py` | Clash, exactly-one, neither, union and sorted reports; membership and nested-loop versus set-intersection timings. Writes `Task04/sets_benchmark.csv`. |
| Task05 | `python Task05/sensor_cleaning.py` | Loop, comprehension and map/filter outputs, alarm minutes, all-valid/all-invalid cases, 10,000 / 100,000 / 1,000,000 reading timings and memory. Writes `Task05/sensor_benchmark.csv`. |
| Task06 | `python Task06/timetable.py` | Five-train timetable, station/day query, sorted departures, unknown-station case, 100 / 1,000 / 10,000 train query benchmark and index memory. Writes `Task06/timetable_benchmark.csv`. |
| Task07 | `python Task07/contact_merge.py` | Normalised phone/email merging, duplicate and missing-field tests, hand-check example, 1,000 / 100,000 contact measurements and pairwise estimate. Writes `Task07/contact_benchmark.csv`. |

Some benchmark tasks process up to one million records. They may take longer than the small demonstration programs. Run from the project root so output CSV paths are correct.

## Evidence workflow

1. Run each program yourself on your Windows laptop.
2. Compare actual output with the expected results described in the task README and report.
3. Capture the complete terminal output using **Win + Shift + S**.
4. Save each screenshot in the matching `TaskXX/evidence/` folder using the exact names in `EVIDENCE_FILENAMES.md`.
5. Keep generated CSV files. The report has measurement tables for you to fill with the results from your own CSV files.
6. Do not present example values or this prepared environment's timings as your own measurements.

## GitHub workflow

Create a public repository named `CSA08-192365059-Assignment3` (or make it private and add your faculty as collaborator). The repository URL is:

`https://github.com/Karthikdj2028/CSA08-192365059-Assignment3`

Commit the README/setup first, then commit Task01 through Task07 separately after running the task and saving evidence. Do not upload all tasks in one final commit.

Example for Task01:

```powershell
git add Task01
git commit -m "feat(task01): analyse rainfall records and moving averages"
git push origin main
```

Use one separate commit for each remaining task. At the end:

```powershell
git log --oneline
git status
```

## Final submission checklist

- [ ] Verify `python --version` is `Python 3.11.6` on the submission computer.
- [ ] Run all seven task programs.
- [ ] Save genuine screenshots in every task evidence folder.
- [ ] Keep all generated benchmark CSV files.
- [ ] Copy actual timing and memory measurements into the report.
- [ ] Commit each task separately and push to GitHub.
- [ ] Confirm the repository is accessible to faculty.
- [ ] Put the repository URL on the report cover and submission portal.

## Assumptions

- Q1 uses deterministic seeded random data for repeatable rainfall examples; the assignment does not supply a real year's data.
- Q3 uses a small stop-word set for the demonstration; a production call-centre system would use a department-approved stop-word list and language-specific tokenisation.
- Q5 treats a sensor error (below -50°C or above 50°C) as invalid and excludes it from the normal-temperature alarm list. A separate sensor-error list is printed.
- Q6 uses a fixed sample railway timetable and synthetic timetables for scaling experiments; the station index is built once and reused for repeated queries.
- Q7 uses a shared normalised phone number as the primary identity signal and normalised email as a fallback when no phone match exists. A matching name alone does not merge contacts because two people can share a name.
