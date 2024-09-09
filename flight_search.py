import os

from dotenv import load_dotenv


class FlightSearch:
    def __init__(self) -> None:
        load_dotenv()
        self._api_key = os.environ("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()

    def fetch_iata(self, city_data: dict) -> dict:
        city_data["iata_code"] = "TESTING"
        return city_data
