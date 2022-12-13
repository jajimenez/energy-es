"""Energy-ES.

Energy-ES is a desktop application that displays the hourly energy prices of
the current day in Spain. The data is provided by the API of Red Electrica.
"""

# We import the "env" module to set a environment variable
from energy_es import env
from energy_es.ui import start_ui


__version__ = "0.1.0"


def main():
    """Application main function."""
    start_ui()
