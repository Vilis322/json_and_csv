from pathlib import Path
from json import load, JSONDecodeError
from csv import DictReader
from logging import getLogger


class DuplicateIDError(Exception):
    """Raises when a duplicate ID is founded."""
    pass


def task3() -> None:
    """Combines employee data from JSON and performance data from CSV to analyze performance statistics.

    This script:
        - Loads and validates employees from 'employees.json', ensuring unique integer IDs.
        - Loads performance data from 'performance.csv', validating structure and uniqueness.
        - Matches employee IDs from both sources, ensuring consistency.
        - Calculates average performance and identifies the employee with the highest score.

    Raises:
        FileNotFoundError: If either input file is missing.
        JSONDecodeError: If the JSON file is malformed.
        DuplicateIDError: If duplicate employee IDs are found in either file.
        KeyError: If required keys are missing in the data.
        TypeError: If an ID is not an integer.
        ValueError: If performance score cannot be converted to an integer.
    """
    print("\n=== TASK 3 STARTS ===")
    logger = getLogger("task3")
    logger.info("Task 3 started")

    # Starts Step 1: reading data from files employees.json and performance.csv
    json_path = Path("employees.json")
    csv_path = Path("performance.csv")

    try:
        if not json_path.exists():
            raise FileNotFoundError(f"File '{json_path}' not found.")
        if not csv_path.exists():
            raise FileNotFoundError(f"File '{csv_path}' not found.")

        with json_path.open(encoding="utf-8") as json_file:
            employees = load(json_file)

        with csv_path.open(encoding="utf-8") as csv_file:
            reader = DictReader(csv_file, skipinitialspace=True)
            performance = list(reader)
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print(f"{e} Check the file and try again.")
            logger.error(e)
        elif isinstance(e, JSONDecodeError):
            logger.error(f"Error parsing the file '{json_path}': {e}")
            print(f"Error while reading employees data in file '{json_path}'. Check the file and try again.")
        else:
            logger.error(f"Failed to parse file '{csv_path}': {e}")
            print(f"Error while reading file '{csv_path}. Check the file and try again.")
        logger.info("Task 3 stopped")
        return

    if not employees:
        logger.warning(f"File '{json_path}' contains no data'")
        logger.info("Task 3 stopped")
        print(f"File '{json_path}' is empty. Check the file and try again.")
        return

    if not performance:
        logger.warning(f"File '{csv_path}' contains no data'")
        logger.info("Task 3 stopped")
        print(f"File '{csv_path}' is empty. Check the file and try again.")
        return

    # Ends Step 1, start Step 2, 3, 4: comparison of performance data for each employee, defining average performance
    # and finding the employee with the highest performance and printing it
    data_error = False
    employees_dict = {}
    json_ids = set()
    for i, employee in enumerate(employees):
        try:
            if "id" not in employee:
                raise KeyError("Missing 'id' key in employee record.")
            employee_id = employee["id"]

            if not isinstance(employee["id"], int):
                raise TypeError(f"ID must be int, got '{type(employee['id'])}' instead.")

            if employee_id in json_ids:
                raise DuplicateIDError(f"Duplicate ID {employee_id} found in employee record #{i}: {employee}")

            json_ids.add(employee_id)
            employees_dict[employee_id] = employee
        except (TypeError, KeyError, DuplicateIDError) as e:
            logger.warning(f"Skipping employee #{i} in JSON due to invalid ID: {e}")
            data_error = True
            continue

    csv_ids = set()
    total_performance = 0
    top_employee = (0, 0)
    for i, row in enumerate(performance):
        try:
            employee_id = int(row["employee_id"])
            performance_score = int(row["performance"])
            if employee_id in csv_ids:
                raise DuplicateIDError(f"Duplicate ID {employee_id} found in employee record #{i}: {row}")
        except (KeyError, ValueError, TypeError, DuplicateIDError) as e:
            logger.warning(f"Skipping employee #{i} in CSV due to invalid data: {e}")
            data_error = True
            continue

        csv_ids.add(employee_id)
        total_performance += performance_score
        if performance_score > top_employee[1]:
            top_employee = (employee_id, performance_score)

    if data_error:
        logger.warning("An invalid data in CSV or in JSON")
        print("An invalid data in CSV or in JSON. Check the logs.")
        if json_ids != csv_ids:
            logger.warning("Mismatch between valid employees in JSON and CSV.")
            logger.warning(f"IDs only in JSON: {sorted(json_ids - csv_ids)}")
            logger.warning(f"IDs only in CSV: {sorted(csv_ids - json_ids)}")
            logger.info("Task 3 stopped")
            print("Mismatch in valid ID data. Check the logs.")
        return

    average_performance = total_performance / len(csv_ids)
    logger.info(f"Average performance: {average_performance}")
    logger.info(f"Top employee ID: {top_employee[0]}")
    print(f"\nAverage performance among all employees: {average_performance}")
    print(f"Top employee name: {employees_dict[top_employee[0]]['name']}")
    print(f"Top employee ID: {top_employee[0]}")
    print(f"Top employee performance: {top_employee[1]}")
    logger.info("Task 3 finished")
    return
