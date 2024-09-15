import os

import requests
from dotenv import load_dotenv


class FlightSearch:
    BASE_API_URL = "https://test.api.amadeus.com"
    TOKEN_ENDPOINT = f"{BASE_API_URL}/v1/security/oauth2/token"
    CITY_ENDPOINT = f"{BASE_API_URL}/v1/reference-data/locations/cities"
    FLIGHT_ENDPOINT = f"{BASE_API_URL}/v2/shopping/flight-offers"

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

    def fetch_iata(self, city_name) -> str:
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

    def check_flights(self, origin_code, destination_code, from_time, to_time):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_code,
            "destinationLocationCode": destination_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(
            url=FlightSearch.FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print(
                "There was a problem with the flight search.\n"
                "For details on status codes, check the API documentation:\n"
                "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                "-reference"
            )
            print("Response body:", response.text)
            return None

        return response.json()
