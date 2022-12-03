"""Energy-ES - Data."""

from datetime import datetime, date

import requests


# Red Electrica API
API_URL = (
    "https://apidatos.ree.es/en/datos/mercados/precios-mercados-tiempo-real?"
    "start_date={}&end_date={}&time_trunc=hour"
)


def get_prices() -> list[dict]:
    """Return the hourly energy prices for the current day in Spain.

    The data is provided by the API of Red Electrica.

    :return: List of dictionaries, where each dictionary contains the
    "datetime" and "value" keys.
    """
    # Prepare URL
    today = date.today().strftime("%Y-%m-%d")
    start = f"{today}00:00"
    end = f"{today}23:59"
    url = API_URL.format(start, end)

    # Make request to the API
    res = requests.get(url)

    # Check response status
    if res.status_code != 200:
        raise Exception(res.reason)

    # Read response data
    data = res.json()["included"]
    prices = list(filter(lambda x: "spot" in x["type"].lower(), data))[0]
    prices = prices["attributes"]["values"]

    # Check data
    if len(prices) != 24:
        raise Exception("Invalid data")

    # Transform data
    prices = list(map(
        lambda x: {
            "datetime": datetime.fromisoformat(x["datetime"].replace(" ", "")),
            "value": x["value"]
        },
        prices
    ))

    # Sort data
    return sorted(prices, key=lambda x: x["datetime"])
