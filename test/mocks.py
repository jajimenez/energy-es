"""Energy-ES - Tests - Data - Mocks."""

from datetime import datetime, date
from unittest.mock import MagicMock
from typing import Any


# "requests.get" method mock
get_mock = MagicMock()
get_mock.return_value.status_code = 200

t = date.today()

spot = [
    {
        "datetime":
            datetime(t.year, t.month, t.day, i).astimezone().isoformat(),
        "value": 1.0
    }
    for i in range(24)
]

pvpc = [
    {
        "datetime":
            datetime(t.year, t.month, t.day, i).astimezone().isoformat(),
        "value": 2.0
    }
    for i in range(24)
]

get_mock.return_value.json.return_value = {
    "included": [
        {
            "type": "spot",
            "attributes": {
                "values": spot
            }
        },
        {
            "type": "pvpc",
            "attributes": {
                "values": pvpc
            }
        }
    ]
}


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
