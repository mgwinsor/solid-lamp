import csv


class DataManager:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.data = []

    def __read_csv(self) -> None:
        """Read the CSV file and store the data in a list of dictionaries."""
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.data = [row for row in reader]

    def get_data(self) -> list[dict]:
        """Return the data read from the CSV file."""
        self.__read_csv()
        return self.data

    def set_data(self, csv_data: list[dict]) -> None:
        """Write the data from a dictionary to the CSV file."""
        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=csv_data[0].keys())
            writer.writeheader()
            writer.writerows(csv_data)
