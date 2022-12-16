"""Energy-ES - Tests - Data - Mocks."""

from datetime import datetime
from unittest.mock import MagicMock
from typing import Any


# Current local datetime
now = datetime.now()

# "requests.get" method mocks
get_spot_mock = MagicMock()
get_spot_mock.status_code = 200

spot = [
    {
        "datetime":
            datetime(now.year, now.month, now.day, i).astimezone().isoformat(),
        "value": 100.10
    }
    for i in range(24)
]

get_spot_mock.json.return_value = {
    "included": [
        {
            "type": "spot",
            "attributes": {
                "values": spot
            }
        }
    ]
}

get_pvpc_mock = MagicMock()
get_pvpc_mock.status_code = 200

pvpc = [
    {
        "Dia": now.strftime("%d/%m/%Y"),
        "Hora": str.zfill(str(i), 2) + "-" + str.zfill(str(i + 1), 2),
        "PCB": "100,25",
        "CYM": "150"
    }
    for i in range(24)
]

get_pvpc_mock.json.return_value = {
    "PVPC": pvpc
}


def requests_get(url: str) -> Any:
    """`requests.get` mock function.

    :param url: Request URL.
    :return: Request response.
    """
    if url.startswith("https://apidatos.ree.es/"):
        return get_spot_mock
    elif url.startswith("https://api.esios.ree.es/"):
        return get_pvpc_mock
    else:
        raise Exception("Invalid URL")


get_mock = MagicMock()
get_mock.side_effect = requests_get


# "userconf.settings.SettingsManager" mock
class SettingsManagerMock:
    """SettingsManager mock."""

    def __init__(self):
        """Initializer."""
        self._data = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value of a setting.

        :param key: Setting key. It must contain at least 1 character and must
        contain and only letters, numbers, hyphens or underscores.
        :param default: Value to return if the setting doesn't exist.
        :return: Setting value or `default`.
        """
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        """Set the value of a setting.

        :param key: Setting key. It must contain at least 1 character and must
        contain only letters, numbers, hyphens or underscores.
        :param value: Setting value. It must be serializable to JSON.
        """
        self._data[key] = value
