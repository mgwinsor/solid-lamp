import os

import requests
from dotenv import load_dotenv


class FlightSearch:
    BASE_API_URL = "https://test.api.amadeus.com/v1"
    TOKEN_ENDPOINT = f"{BASE_API_URL}/security/oauth2/token"
    CITY_ENDPOINT = f"{BASE_API_URL}/reference-data/locations/cities"

    def __init__(self) -> None:
        load_dotenv()
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        response = requests.post(
            url=FlightSearch.TOKEN_ENDPOINT,
            headers=header,
            data=body,
        )
        print(response.json()["access_token"])
        return response.json()["access_token"]

    def fetch_iata(self, city_data: dict) -> dict:
        city_data["iata_code"] = "TESTING"
        return city_data
