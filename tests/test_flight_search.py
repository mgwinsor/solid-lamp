import pytest
import requests_mock

from src.flight_search import FlightSearch


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("AMADEUS_API_KEY", "test_key")
    monkeypatch.setenv("AMADEUS_API_SECRET", "test_secret")


@pytest.fixture
def city_name_data():
    return "Paris"


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


def test_get_iata(flight_search, city_name_data):
    expected_headers = {
        "Authorization": f"Bearer {flight_search._token}",
    }
    mock_response = {
        "data": [
            {"name": "Paris", "iataCode": "PAR"},
        ],
    }

    with requests_mock.Mocker() as mock:
        mock.get(
            url=FlightSearch.CITY_ENDPOINT,
            headers=expected_headers,
            json=mock_response,
        )
        result = flight_search.fetch_iata(city_name_data)
        request_headers = mock.last_request.headers

    assert request_headers["Authorization"] == expected_headers["Authorization"]

    expected = "PAR"
    assert result == expected
