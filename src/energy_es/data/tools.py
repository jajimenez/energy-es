"""Energy-ES - Data - Tools."""

from datetime import datetime


def get_time(dt: datetime) -> str:
    """Return the time information of a datetime as a HH:MM string.

    :param dt: Datetime.
    :return: Time as a string.
    """
    return dt.strftime("%H:%M")
