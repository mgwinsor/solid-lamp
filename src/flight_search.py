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
        self._token: str = None

    def get_new_token(self) -> None:
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
        self._token = response.json()["access_token"]

    def fetch_iata(self, city_name) -> dict:
        headers = {"Authorization": f"Bearer {self._token}"}
        body = {
            "keyword": city_name,
            "max": 1,
            "include": "AIRPORTS",
        }
        response = requests.get(
            url=FlightSearch.CITY_ENDPOINT,
            headers=headers,
            params=body,
        )

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            iata_code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return iata_code
