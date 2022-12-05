"""Energy-ES - Data."""

from datetime import datetime, date

import requests
import userconf as uc


class PricesManager:
    """Prices manager.

    This class gets the hourly energy prices of the current day in Spain. The
    data is cached in a configuration file inside the user's home directory.

    The data is provided by the API of Red Electrica.
    """

    # Red Electrica API
    API_URL = (
        "https://apidatos.ree.es/en/datos/mercados/precios-mercados-tiempo-"
        "real?start_date={}&end_date={}&time_trunc=hour"
    )

    def __init__(self):
        """Class initializer.

        When this method is called, the `_load_data` method is called.
        """
        self.conf = uc.Userconf("energy_es")
        self._load_data()

    def _load_data(self):
        """Load the data from the cache."""
        self._date = self.conf.get("date")
        self._prices = self.conf.get("prices")

    def _save_data(self):
        """Save the data to the cache."""
        self.conf.set("date", self._date)
        self.conf.set("prices", self._prices)

    def _is_data_valid(self) -> bool:
        """Check if the data is valid or not.

        :return: Whether the data is valid or not.
        """
        return self._date == str(date.today()) and self._prices is not None

    def _update_data(self):
        """Update the data by calling the API."""
        # Get current day
        today = date.today().strftime("%Y-%m-%d")

        # Prepare URL
        start = f"{today}00:00"
        end = f"{today}23:59"
        url = PricesManager.API_URL.format(start, end)

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
                "hour":
                    datetime.fromisoformat(x["datetime"].replace(" ", ""))
                    .strftime("%H:%M"),
                "value": x["value"]
            },
            prices
        ))

        # Sort data
        prices = sorted(prices, key=lambda x: x["hour"])

        # Update date and prices
        self._date = today
        self._prices = prices

    def get_prices(self) -> list[dict]:
        """Return the hourly energy prices of the current day in Spain.

        :return: List of dictionaries, where each dictionary contains the
        "hour" (string) and "value" (float) keys.
        """
        if not self._is_data_valid():
            self._update_data()
            self._save_data()

        return self._prices

    def get_min_price(self) -> dict:
        """Return the minimum price of the current day in Spain.

        :return: Dictionary containing the "hour" (string) and "value" (float)
        keys.
        """
        return min(self.get_prices(), key=lambda x: x["value"])

    def get_max_price(self) -> dict:
        """Return the maximum price of the current day in Spain.

        :return: Dictionary containing the "hour" (string) and "value" (float)
        keys.
        """
        return max(self.get_prices(), key=lambda x: x["value"])
