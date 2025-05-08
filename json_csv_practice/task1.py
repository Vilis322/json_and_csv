from pathlib import Path
from json import load, JSONDecodeError
from logging import getLogger


def task1() -> None:
    """Analyzes student data from a JSON file and displays key statistics.

    Loads student data from 'students.json', logs errors if the file is missing
    or corrupted, and performs three main operations:
        - Displays the total number of students.
        - Finds and prints the oldest student with valid age data.
        - Prompts the user for a subject name and displays how many students study that subject.
        Allows repeated input until a match or 'exit'.

    Raises:
    FileNotFoundError: If the file 'students.json' is not found.
    JSONDecodeError: If the file contains invalid JSON.
    KeyError: If a student dictionary is missing required fields.
    TypeError: If a student's age has an invalid type.
    """
    print("\n=== TASK 1 STARTS ===")
    logger = getLogger("task1")
    logger.info("Task 1 started")

    file_path = Path("students.json")  # Starts Step 1: reading data from file

    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' not found.")

        with file_path.open(encoding="utf-8") as file:
            students = load(file)
    except (FileNotFoundError, JSONDecodeError) as e:
        if isinstance(e, FileNotFoundError):
            logger.error(f"Error opening file '{file_path}': {e}")
            print(f"{e} Check the path and try again.")
        elif isinstance(e, JSONDecodeError):
            logger.error(f"Error reading file '{file_path}': {e.msg} at line {e.lineno}, column {e.colno}")
            print(f"An error within reading the file '{file_path}'")
        logger.info("Task 1 stopped")
        return

    if not students:
        logger.warning(f"File {file_path} loaded, but student list is empty")
        logger.info("Task 1 stopped")
        print(f"File '{file_path}' is empty. Check the file and try again.")
        return

    print(f"\nTotal count of students: {len(students)}")  # Ends Step 1, starts Step 2: counting amount of students

    valid_students = []  # Ends Step 2, starts Step 3: finding the oldest student and printing his data (name, age etc.)

    for i, student in enumerate(students):
        try:
            age = student['age']
            if not isinstance(age, int):
                raise TypeError(f"Invalid type for age: {type(age)}")
            valid_students.append(student)
        except (KeyError, TypeError) as e:
            logger.warning(f"Error in element #{i}: {e}. Student data: {student}")
            continue

    if not valid_students:
        logger.warning("There is no valid student list with valid key 'age'")
        logger.info("Task 1 stopped")
        print("There is no valid student list with valid age. Check the file and try again.")
        return

    oldest_student = max(valid_students, key=lambda student: student["age"])
    print(f"\nThe oldest student is {oldest_student['name']}.")
    print(f"His age is {oldest_student['age']}.")
    print(f"He is from {oldest_student['city']}")

    all_subjects = set()  # Ends Step 3, starts Step 4: counting amount of student who learning certain subject
    for student in students:
        all_subjects.update(subject.lower() for subject in student.get("subjects", []))

    subject = ""
    while subject != "exit":
        subject = input("\nEnter a subject name to analyze or 'exit' to stop Task 1: ").strip().lower()

        if subject == "exit":
            logger.info("Task 1 stopped by user request")
            print("Exiting Task 1.")
            return

        if subject in all_subjects:
            count = sum(
                subject in (s.lower() for s in student.get("subjects", []))
                for student in students
            )
            print(f"{count} student{'s' if count > 1 else ''} study '{subject}'.")
            logger.info("Task 1 finished")
            return
        else:
            print(f"No students study '{subject}'. Try again or type 'exit'.")
            logger.warning(f"Subject '{subject}' not found among students")
