"""Energy-ES - Data - Prices."""

from datetime import datetime, date

import requests
from userconf import UserConf


class PricesManager:
    """Prices manager.

    This class gets the hourly energy prices of the current day in Spain. The
    data is cached in a configuration file inside the user's home directory.

    The prices are stored in €/MWh but can be returned by the
    `get_spot_market_prices` and `get_pvpc_prices` methods in either €/MWh or
    €/KWh.

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
        self._conf = UserConf("energy_es")

        # Data
        self._spot = None  # Spot Market prices in €/MWh
        self._pvpc = None  # PVPC prices in €/MWh

        self._load_data()

    def _load_data(self):
        """Load the data from the cache."""
        spot = self._conf.settings.get("spot_market_prices")
        pvpc = self._conf.settings.get("pvpc_prices")
        prices = []

        for i in (spot, pvpc):
            i2 = i

            if i2 is not None:
                i2 = list(map(
                    lambda x: {
                        "datetime": datetime.fromisoformat(x["datetime"]),
                        "value": x["value"]
                    },
                    i2
                ))

            prices.append(i2)

        self._spot, self._pvpc = prices

    def _save_data(self):
        """Save the data to the cache."""
        prices = []

        for i in (self._spot, self._pvpc):
            i2 = i

            if i2 is not None:
                i2 = list(map(
                    lambda x: {
                        "datetime": x["datetime"].isoformat(),
                        "value": x["value"]
                    },
                    i2
                ))

            prices.append(i2)

        self._conf.settings.set("spot_market_prices", prices[0])
        self._conf.settings.set("pvpc_prices", prices[1])

    def _is_data_valid(self) -> bool:
        """Check if the data is valid.

        :return: Whether the data is valid.
        """
        if self._spot is None or self._pvpc is None:
            return False

        # Get last data datetime (which has already its UTC offset information)
        # and the current local datetime. We call "astimezone" to convert the
        # local datetime to the same datetime but with its time zone
        # information (UTC offset and time zone name). This way, we can compare
        # both datetimes.

        # Last data datetime, with UTC offset
        d1 = self._spot[0]["datetime"]

        # Local datetime, with UTC offset
        d2 = datetime.now().astimezone()

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

        # Spot market prices (in €/MWh)
        spot = list(filter(lambda x: "spot" in x["type"].lower(), data))[0]
        spot = spot["attributes"]["values"]

        # PVPC prices (in €/MWh)
        pvpc = list(filter(lambda x: "pvpc" in x["type"].lower(), data))[0]
        pvpc = pvpc["attributes"]["values"]

        # Check data
        if len(spot) != 24 or len(pvpc) != 24:
            raise Exception("Invalid data")

        # Transform and sort data
        prices = []

        for i in (spot, pvpc):
            i2 = list(map(
                lambda x: {
                    "datetime":
                        datetime.fromisoformat(x["datetime"].replace(" ", "")),
                    "value": x["value"]
                },
                i
            ))

            i2 = sorted(i2, key=lambda x: x["datetime"])
            prices.append(i2)

        # Update prices
        self._spot, self._pvpc = prices

        # Save data
        self._save_data()

    def _get_prices(self, var: str = "spot", unit: str = "m") -> list[dict]:
        """Return the hourly energy prices (of either Spot Market or PVPC) of
        the current day in Spain.

        :param var: Prices variable. It must be "spot" to return the Spot
        Market prices or "pvpc" to return the PVPC prices.
        :param unit: Prices unit. It must be "k" to return the prices in €/KWh
        or "m" (default) to return them in €/MWh.
        :return: List of dictionaries, where each dictionary contains the
        "datetime" (datetime) and "value" (float) keys.
        """
        var = var.lower()

        # Check variable
        if var not in ("spot", "pvpc"):
            raise Exception(
                'Invalid variable. It must be "spot" (Spot Market prices) or '
                '"pvpc" (PVPC prices)'
            )

        unit = unit.lower()

        # Check units
        if unit not in ("k", "m"):
            raise Exception(
                'Invalid unit. It must be "k" (€/KWh) or "m" (€/MWh)'
            )

        # Check whether data is valid
        if not self._is_data_valid():
            self._update_data()

        # Choose data
        data = self._spot if var == "spot" else self._pvpc

        if unit == "m":
            # Deep copy of "data" (in €/MWh)
            data = [i.copy() for i in data]
        else:
            # Deep copy of "data" with the prices in €/KWh
            data = list(map(
                lambda x: {
                    "datetime": x["datetime"],
                    "value": round(x["value"] / 1000, 4)
                },
                data
            ))

        return data

    def get_spot_market_prices(self, unit: str = "m") -> list[dict]:
        """Return the hourly energy Spot Market prices of the current day in
        Spain.

        :param units: "k" to return the prices in €/KWh or "m" (default) to
        return them in €/MWh.
        :param unit: Prices unit. It must be "k" to return the prices in €/KWh
        or "m" (default) to return them in €/MWh.
        :return: List of dictionaries, where each dictionary contains the
        "datetime" (datetime) and "value" (float) keys.
        """
        return self._get_prices("spot", unit)

    def get_pvpc_prices(self, unit: str = "m") -> list[dict]:
        """Return the hourly energy PVPC prices of the current day in Spain.

        :param units: "k" to return the prices in €/KWh or "m" (default) to
        return them in €/MWh.
        :param unit: Prices unit. It must be "k" to return the prices in €/KWh
        or "m" (default) to return them in €/MWh.
        :return: List of dictionaries, where each dictionary contains the
        "datetime" (datetime) and "value" (float) keys.
        """
        return self._get_prices("pvpc", unit)
