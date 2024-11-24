import csv
from pathlib import Path
from time import sleep
import logging

logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class MyError(Exception):
    def __init__(self, text):
        super().__init__(text)


def from_txt_to_csv(input_file, output_file='output.csv'):
    text_file = Path(input_file).read_text(encoding='utf8').splitlines()

    with open(output_file, 'w', newline='', encoding='utf8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        csv_writer.writerow(['Name', 'Amount', 'Price per piece'])

        for line in text_file:
            try:
                items = line.split('\t')
                if len(items) != 3:
                    raise MyError(f"The line {line} is an invalid, skipping this line.")

                item, quantity, price = items
                csv_writer.writerow([item, quantity, price])
            except MyError as e:
                logging.error(e)

        return output_file


def calculate_total_cost(input_file):
    with open(input_file, 'r', encoding='utf8') as csv_file:
        csv_file = csv.reader(csv_file, delimiter=',')
        next(csv_file)
        total_cost = 0

        for index_line, line in enumerate(csv_file, 1):
            try:
                item, quantity, price = line[0], line[1], line[2]
                if not quantity.isdigit() and not price.isdigit():
                    raise ValueError()

                item_cost = int(quantity) * int(price)
                print(f"{item} will cost {item_cost} EUR per {quantity} items.")
                sleep(2)
                total_cost += item_cost
            except ValueError as e:
                print(f"In line {index_line}, the quantity or/and price wasn't/weren't as a number.")
                sleep(2)
                logging.error(f"Invalid line {index_line}: {e}")

        return total_cost


def main():
    csv_file = from_txt_to_csv('prices.txt')
    total_cost = calculate_total_cost(csv_file)

    print(f"Cost for all items will be {total_cost} EUR.")


if __name__ == '__main__':
    main()
