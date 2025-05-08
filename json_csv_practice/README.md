# *JSON & CSV TASKS*

## *DESCRIPTION*
+ This project consists of three independent Python scripts that process structured data from JSON and CSV files. The tasks are logically connected but can be executed individually. All tasks are launched via the central `main.py` script, which provides an interface for selecting and executing them in any order and as many times as needed.

---

## *TASKS DESCRIPTION*

### Task 1 — Student Data Analysis (`task1.py`)
- Loads student records from `students.json`.
- Outputs:
  - total number of students;
  - the oldest student with valid age information;
  - number of students studying a subject provided by the user.

### Task 2 — Sales Data Processing (`task2.py`)
- Loads sales records from `sales.csv`.
- Calculates and displays:
  - total sales amount;
  - top-selling item;
  - monthly breakdown of total sales.

### Task 3 — Employee Performance Matching (`task3.py`)
- Merges data from `employees.json` and `performance.csv`.
- Validates IDs, matches employees with their performance scores.
- Computes:
  - average performance;
  - top-performing employee.

---

## *REQUIREMENTS*

+ **Python 3.10** or higher