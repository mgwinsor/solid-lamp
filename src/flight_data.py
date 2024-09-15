class FlightData:
    """This class is responsible for structuring the flight data."""

    def __init__(self, price, origin, destination, out_date, return_date):
        self.price = price
        self.origin_airport = origin
        self.destination_airport = destination
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data):
    if data is None or not data["data"]:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = data["data"][0]
    lowest_price = float(first_flight["price"]["grandTotal"])

    itineraries = first_flight["itineraries"]
    origin = itineraries[0]["segments"][0]["departure"]["iataCode"]
    destination = itineraries[0]["segments"][0]["arrival"]["iataCode"]
    out_date = itineraries[0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = itineraries[1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(
        lowest_price,
        origin,
        destination,
        out_date,
        return_date,
    )

    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price

            itineraries = flight["itineraries"]
            outbound_segments = itineraries[0]["segments"][0]
            return_segments = itineraries[1]["segments"][0]

            origin = outbound_segments["departure"]["iataCode"]
            destination = outbound_segments["arrival"]["iataCode"]
            out_date = outbound_segments["departure"]["at"].split("T")[0]
            return_date = return_segments["departure"]["at"].split("T")[0]

            cheapest_flight = FlightData(
                lowest_price,
                origin,
                destination,
                out_date,
                return_date,
            )
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight
