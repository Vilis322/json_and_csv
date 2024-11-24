from converter import CsvJsonConverter


def main():
    CsvJsonConverter.printing_info()
    file = input("Enter the name of the file which you want to convert: ").lower().strip()
    converting_file = CsvJsonConverter(file)

    try:
        if CsvJsonConverter.suffix_file(file) == ".json":
            filename = input("Enter the name of the CSV converted file: ").strip()
            converting_file.convert_to_csv(filename)
        elif CsvJsonConverter.suffix_file(file) == ".csv":
            filename = input("Enter the name of the JSON converted file: ").strip()
            converting_file.convert_to_json(filename)
    except AttributeError:
        print("You entered an invalid file format. Please try again.")


if __name__ == "__main__":
    main()
