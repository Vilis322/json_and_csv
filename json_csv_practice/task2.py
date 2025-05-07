from pathlib import Path
from csv import DictReader
from collections import defaultdict
from logging import getLogger
from datetime import datetime


def task2() -> None:
    """Analyzes sales data from a CSV file and displays key statistics.

    Reads data from 'sales.csv', processes each row, and displays:
      - Total sum of all sales.
      - Top-selling item with its cumulative sales.
      - Total sales amount per month.

    Invalid or incomplete rows (e.g., missing keys, bad data types, or wrong date format)
    are skipped with a warning logged. The function assumes the date format to be '%Y-%m-%d'.

    The function logs all critical steps and skips incorrect rows without interrupting execution.

    Raises:
        FileNotFoundError: If 'sales.csv' is not found.
        ValueError: If a row contains invalid numeric or date format in 'Sum' or 'Date' fields.
        KeyError: If required keys ('Item', 'Sum', 'Date') are missing in any row.
    """
    print("\n=== TASK 2 STARTS ===")
    logger = getLogger("task2")
    logger.info("Task 2 started")

    file_path = Path("sales.csv")  # Starts Step 1: reading data from file

    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' not found.")

        with file_path.open(encoding='utf-8') as file:
            reader = DictReader(file, skipinitialspace=True)
            sales = list(reader)
    except FileNotFoundError as e:
        logger.error(f"Error opening file '{file_path}': {e}")
        print(f"{e} Check the file path and try again.")
        return
    except Exception as e:
        logger.error(f"Error reading file '{file_path}': {e}")
        print(f"An error occurred while reading file '{file_path}'. Check the file and try again.")
        return

    if not sales:
        logger.warning("Sales file loaded but contains no data")
        logger.info("Task 2 stopped")
        print(f"File '{file_path}' is empty. Check the file and try again.")
        return

    # Ends Step 1, starts Step 2, 3, 4: counting amount of sales during the whole period,
    # defining top-selling item, dividing sales by months and printing it
    total_sales = 0
    total_sale_per_item = defaultdict(int)
    monthly_total_sales = defaultdict(int)

    for i, row in enumerate(sales):
        try:
            item = row["Item"]
            amount = int(row["Sum"])
            date = row["Date"]
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            monthly_key = date_obj.strftime("%Y-%m")

            total_sales += amount
            total_sale_per_item[item] += amount
            monthly_total_sales[monthly_key] += amount
        except (KeyError, ValueError) as e:
            logger.warning(f"Skipping invalid row #{i}: {e}. Row: {row}")
            continue

    top_item = max(total_sale_per_item.items(), key=lambda x: x[1])
    logger.info(f"Top-selling item is '{top_item[0]}' with total sales of {top_item[1]}")
    print(f"\nTotal sales sum: {total_sales}¥")
    print(f"\nTop-selling item: {top_item[0]}. Total sales: {top_item[1]}¥")
    print(f"\nMonthly sales totals:")
    for month, amount in sorted(monthly_total_sales.items()):
        print(f"{month}: {amount}¥")
    logger.info("Task 2 finished")
