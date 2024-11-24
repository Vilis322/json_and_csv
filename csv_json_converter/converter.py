import json
import csv
import mimetypes
from pathlib import Path
import logging
from time import sleep


logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class EmptyFileException(Exception):
    def __init__(self):
        super().__init__("Empty file.")


class IncorrectJsonItem(Exception):
    def __init__(self):
        super().__init__("Item is not a dict.")


class CsvJsonConverter:
    def __init__(self, file):
        self.file = Path(file)
        self.json_data = []
        self.csv_data = []

    def load_data(self):
        mime_type, _ = mimetypes.guess_type(self.file)
        try:
            if self.file.stat().st_size == 0:
                raise EmptyFileException

            if mime_type == "application/json":
                with open(self.file, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    for item in data:
                        if isinstance(item, dict):
                            self.json_data.append(item)

            if mime_type == "text/csv" or self.file.name.endswith('.csv'):
                with open(self.file, 'r', newline='', encoding='utf-8') as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=',')
                    for row in reader:
                        self.csv_data.append(row)

            return True
        except FileNotFoundError as e:
            print("File not found. Try again.")
            logging.error(f"File not found: {e}")
            return False
        except json.JSONDecodeError as e:
            print("Invalid JSON file. Please check the file and try again.")
            logging.error(f"Invalid JSON: {e}")
            return False
        except csv.Error as e:
            print("Invalid CSV file. Please check the file and try again.")
            logging.error(f"Invalid CSV format: {e}")
            return False
        except EmptyFileException as e:
            print("File cannot be an empty. PLease check the file and try again.")
            logging.error(f"{e}")
            return False

    def convert_to_csv(self, csv_filename):
        output_path = Path(csv_filename)
        if output_path.suffix != ".csv":
            output_path = output_path.with_suffix(".csv")

        if not self.load_data():
            print("No data to convert. Something went wrong. Please check the file and try again.")
            return

        CsvJsonConverter.create_directory(output_path)
        headers = list(self.json_data[0].keys())
        for item in self.json_data:
            for key in item.keys():
                if key not in headers:
                    headers.append(key)

        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                for item in self.json_data:
                    row = {key: item.get(key, '') for key in headers}
                    writer.writerow(row)
        except PermissionError as e:
            print(f"You don't have a permission for write to the file {output_path.name}. Please try again.")
            logging.error(f"Don't have permission: {e}")
        except OSError as e:
            print(f"OS error. Something went wrong. Please try again.")
            logging.error(f"OS error during file writing: {e}. Path: {output_path}")

    def convert_to_json(self, json_filename):
        output_path = Path(json_filename)
        if output_path.suffix != ".json":
            output_path = output_path.with_suffix(".json")

        if not self.load_data():
            print("No data to convert. Something went wrong. Please check the file and try again.")
            return

        CsvJsonConverter.create_directory(output_path)

        try:
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(self.csv_data, json_file, ensure_ascii=False, indent=4)
        except PermissionError as e:
            print(f"You don't have a permission for write to the file {output_path.name}. Please try again.")
            logging.error(f"Don't have permission: {e}")
        except OSError as e:
            print(f"OS error. Something went wrong. Please try again.")
            logging.error(f"OS error during file writing: {e}. Path: {output_path}")

    @staticmethod
    def create_directory(path):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            parent_dir = path.parent.absolute()
            print(f"File in directory {parent_dir} successfully created.")
            return path.parent
        except FileExistsError as e:
            print(f"File with name {path} already exists. Please check the name and try again.")
            logging.error(f"File already exists: {e}")
        except PermissionError as e:
            print(f"You don't have a permission for creating directory in this location. Please chose other directory.")
            logging.error(f"Don't have permission: {e}")
        except OSError as e:
            print(f"OS error. Something went wrong. Please check the name of the file and try again.")
            logging.error(f"OS error: {e}")

    @staticmethod
    def suffix_file(file):
        if file.endswith(".csv"):
            return ".csv"
        elif file.endswith(".json"):
            return ".json"

    @staticmethod
    def printing_info():
        print("Welcome to CSV JSON converter!")
        sleep(3)
        print("You can convert JSON file to CSV file and opposite.")
        sleep(3)
        print("You have to enter the file, which you want to convert, with right suffix (.csv or .json).")
        sleep(3)
        print("After checking if file exists you have to enter a name of new file with or without suffix.")
        sleep(3)
        print("Also you can enter a different directory for new file, but it has to be in correct format.")
        sleep(3)
        print("After all the checks if they were successful the program converts the data to the new file.\n")
        sleep(3)
