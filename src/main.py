import time
from datetime import datetime, timedelta
from pathlib import Path

from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch

ORIGIN_CITY_IATA = "LON"

if __name__ == "__main__":
    csv_file = DataManager(file_path=Path("./data/flight_deal_prices.csv"))
    data = csv_file.get_data()

    flights = FlightSearch()
    flights.get_new_token()
    for row in data:
        row["iata_code"] = flights.fetch_iata(city_name=row["city"])
        time.sleep(2)
    csv_file.set_data(data)

    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

    for destination in data:
        print(f"Getting flights for {destination['city']}...")
        flight_details = flights.check_flights(
            ORIGIN_CITY_IATA,
            destination["iata_code"],
            from_time=tomorrow,
            to_time=six_month_from_today,
        )
        cheapest_flight = find_cheapest_flight(flight_details)
        print(f"{destination['city']}: £{cheapest_flight.price}")
        # Slowing down requests to avoid rate limit
        time.sleep(2)
