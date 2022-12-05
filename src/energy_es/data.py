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
        prices = self.conf.get("prices")

        if prices is not None:
            prices = list(map(
                lambda x: {
                    "datetime": datetime.fromisoformat(x["datetime"]),
                    "value": x["value"]
                },
                prices
            ))

        self._prices = prices

    def _save_data(self):
        """Save the data to the cache."""
        prices = list(map(
            lambda x: {
                "datetime": x["datetime"].isoformat(),
                "value": x["value"]
            },
            self._prices
        ))

        self.conf.set("prices", prices)

    def _is_data_valid(self) -> bool:
        """Check if the data is valid or not.

        :return: Whether the data is valid or not.
        """
        if self._prices is None:
            return False

        # Get last data datetime (which has already its UTC offset information)
        # and the current local datetime. We call "astimezone" to convert the
        # local datetime to the same datetime but with its time zone
        # information (UTC offset and time zone name). This way, we can compare
        # both datetimes.
        d1 = self._prices[0]["datetime"]  # Last data datetime, with UTC offset
        d2 = datetime.now().astimezone()  # Local datetime, with UTC offset

        # Clear time
        d1 = d1.replace(hour=0, minute=0, second=0, microsecond=0)
        d2 = d2.replace(hour=0, minute=0, second=0, microsecond=0)

        # Compare dates (datetimes with the same time and UTC offset)
        return d1 == d2

    def _update_data(self):
        """Update the data by calling the API."""
        # Get current day (in the local time zone). We don't need to convert it
        # to a datetime of any time zone of Spain as the API requires input
        # start and end datetimes but ignores them and always returns the data
        # for the current day in Spain (in the Europe/Madrid time zone).
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
                "datetime":
                    datetime.fromisoformat(x["datetime"].replace(" ", "")),
                "value": x["value"]
            },
            prices
        ))

        # Sort data
        prices = sorted(prices, key=lambda x: x["datetime"])

        # Update prices
        self._prices = prices

        # Save data
        self._save_data()

    def get_prices(self) -> list[dict]:
        """Return the hourly energy prices of the current day in Spain.

        :return: List of dictionaries, where each dictionary contains the
        "hour" (string) and "value" (float) keys.
        """
        if not self._is_data_valid():
            self._update_data()

        return self._prices
