import pytest
import requests_mock

from src.flight_search import FlightSearch


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("AMADEUS_API_KEY", "test_key")
    monkeypatch.setenv("AMADEUS_API_SECRET", "test_secret")


@pytest.fixture
def flight_deal_data():
    return [
        {"city": "Paris", "iata_code": "", "lowest_price": 54},
        {"city": "Tokyo", "iata_code": "", "lowest_price": 485},
        {"city": "Hong Kong", "iata_code": "", "lowest_price": 551},
    ]


@pytest.fixture
def flight_search(mock_env_vars):
    return FlightSearch()


def test_initialization(flight_search):
    assert flight_search._api_key == "test_key"
    assert flight_search._api_secret == "test_secret"
    assert flight_search._token is None


def test_get_new_token(flight_search):
    with requests_mock.Mocker() as mock:
        mock.post(FlightSearch.TOKEN_ENDPOINT, json={"access_token": "mock_token"})
        flight_search.get_new_token()
        assert flight_search._token == "mock_token"


def test_get_iata(flight_search, flight_deal_data):
    mock_response = {
        "data": [
            {"name": "Paris", "iataCode": "PAR"},
        ],
    }
    with requests_mock.Mocker() as mock:
        mock.get(FlightSearch.CITY_ENDPOINT, json=mock_response)
    expected = [
        {"city": "Paris", "iata_code": "PAR", "lowest_price": 54},
        {"city": "Tokyo", "iata_code": "TYO", "lowest_price": 485},
        {"city": "Hong Kong", "iata_code": "HKG", "lowest_price": 551},
    ]
    result = flight_search.fetch_iata(flight_deal_data)
    assert result == expected
