from pathlib import Path

from data_manager import DataManager
from flight_search import FlightSearch

if __name__ == "__main__":
    csv_file = DataManager(file_path=Path("./data/flight_deal_prices.csv"))
    data = csv_file.get_data()

    flights = FlightSearch()
    city = [flights.fetch_iata(city) for city in data if city["iata_code"] == ""]
    csv_file.set_data(data)
