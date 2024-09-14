import time
from pathlib import Path

from data_manager import DataManager
from flight_search import FlightSearch

if __name__ == "__main__":
    csv_file = DataManager(file_path=Path("./data/flight_deal_prices.csv"))
    data = csv_file.get_data()

    flights = FlightSearch()
    flights.get_new_token()
    for row in data:
        row["iata_code"] = flights.fetch_iata(city_name=row["city"])
        time.sleep(2)
    csv_file.set_data(data)
