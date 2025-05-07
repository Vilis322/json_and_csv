from pathlib import Path
from json import load, JSONDecodeError
from logging import getLogger


def task1() -> None:
    """"""
    print("\n=== TASK 1 STARTS ===")
    logger = getLogger("task1")
    logger.info("Task 1 started")

    file_path = Path("students.json")

    try:
        if not file_path.exists():
            raise FileNotFoundError("File 'students.json' not found.")

        with file_path.open(encoding="utf-8") as file:
            students = load(file)
    except FileNotFoundError as e:
        logger.error(f"Error opening file '{file_path}': {e}")
        print(f"{e} Check the path and try again.")
        return
    except JSONDecodeError as e:
        logger.error(f"Error reading file '{file_path}': {e.msg} at line {e.lineno}, column {e.colno}")
        print("An error within reading the file 'students.json'")
        return

    if not students:
        logger.warning("File loaded, but student list is empty.")
        logger.info("Task 1 stopped.")
        print("File 'students.json' is empty. Check the file and try again.")
        return

    print(f"\nTotal count of students: {len(students)}")

    valid_students = []

    for i, student in enumerate(students):
        try:
            age = student['age']
            if not isinstance(age, int):
                raise TypeError(f"Invalid type for age: {type(age)}")
            valid_students.append(student)
        except (KeyError, TypeError) as e:
            logger.error(f"Error in element #{i}: {e}. Student data: {student}")

    if not valid_students:
        logger.warning("There is no valid student list with valid key 'age'.")
        logger.info("Task 1 stopped.")
        print("There is no valid student list with valid age. Check the file and try again.")
        return

    oldest_student = max(valid_students, key=lambda student: student["age"])
    print(f"\nThe oldest student is {oldest_student['name']}.")
    print(f"His age is {oldest_student['age']}.")
    print(f"He is from {oldest_student['city']}")

    all_subjects = set()
    for student in students:
        all_subjects.update(subject.lower() for subject in student.get("subjects", []))

    subject = ""
    while subject != "exit":
        subject = input("\nEnter a subject name to analyze or 'exit' to stop Task 1: ").strip().lower()

        if subject == "exit":
            logger.info("Task 1 stopped by user request.")
            print("Exiting Task 1.")
            return

        if subject in all_subjects:
            count = sum(
                subject in (s.lower() for s in student.get("subjects", []))
                for student in students
            )
            print(f"{count} student{'s' if count > 1 else ''} study '{subject}'.")
            logger.info("Task 1 finished.")
            return
        else:
            print(f"No students study '{subject}'. Try again or type 'exit'.")
            logger.warning(f"Subject '{subject}' not found among students.")
