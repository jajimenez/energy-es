"""Energy-ES - Tests - Data - Prices - Unit tests."""

from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch

# We import "paths" to include the "src" directory in "sys.path" so that we can
# import "userconf".
import paths
from mocks import get_mock, SettingsManagerMock

from energy_es.data.prices import PricesManager


class DataPricesTestCase(unittest.TestCase):
    """Unit tests of the "energy_es.data.prices" module."""

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_initial_data(self, sm_mock: MagicMock):
        """Test the initial values of `PricesManager._spot` and
        `PricesManager._pvpc`.
        """
        # MagicMock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()

        spot = pm._spot
        pvpc = pm._pvpc

        self.assertIs(spot, None)
        self.assertIs(pvpc, None)

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_is_data_valid(self, sm_mock: MagicMock):
        """Test `PricesManager._is_data_valid`."""
        # MagicMock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        self.assertFalse(pm._is_data_valid())

        pm.get_spot_market_prices()
        self.assertTrue(pm._is_data_valid())

    def _check_prices(self, prices: list[dict]):
        self.assertIs(type(prices), list)
        self.assertEqual(len(prices), 24)

        for i in prices:
            self.assertIs(type(i), dict)
            self.assertEqual(len(i), 2)

            self.assertTrue("datetime" in i)
            self.assertTrue("value" in i)

            self.assertIs(type(i["datetime"]), datetime)
            self.assertIs(type(i["value"]), float)

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_get_spot_market_prices(self, sm_mock: MagicMock):
        """Test the value returned by `PricesManager.get_spot_market_prices`.
        """
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        spot = pm.get_spot_market_prices()
        self._check_prices(spot)

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_get_pvpc_prices(self, sm_mock: MagicMock):
        """Test the value returned by `PricesManager.get_pvpc_prices`."""
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        pvpc = pm.get_pvpc_prices()
        self._check_prices(pvpc)

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    @patch("energy_es.data.prices.PricesManager._get_prices")
    def test_get_prices_1(
        self, gp_mock: MagicMock, sm_mock: MagicMock
    ):
        """Test `PricesManager.get_prices` calls in
        `PricesManager.get_spot_market_prices`.
        """
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        gp_mock.assert_not_called()

        pm.get_spot_market_prices()
        gp_mock.assert_called_once()

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    @patch("energy_es.data.prices.PricesManager._get_prices")
    def test_get_prices_2(
        self, gp_mock: MagicMock, sm_mock: MagicMock
    ):
        """Test `PricesManager.get_prices` calls in
        `PricesManager.get_pvpc_prices`.
        """
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()
        gp_mock.assert_not_called()

        pm.get_pvpc_prices()
        gp_mock.assert_called_once()

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_spot_market_prices_units(self, sm_mock: MagicMock):
        """Test the the values returned by
        `PricesManager.get_spot_market_prices` in different units.
        """
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()

        spot_k = pm.get_spot_market_prices("k")
        spot_m = pm.get_spot_market_prices("m")

        k_count = len(spot_k)
        m_count = len(spot_m)

        self.assertEqual(k_count, 24)
        self.assertEqual(m_count, 24)

        for i in range(k_count):
            act = spot_k[i]["value"]
            exp = round(spot_m[i]["value"] / 1000, 5)

            self.assertEqual(act, exp)

    @patch("requests.get", get_mock)
    @patch("userconf.SettingsManager")
    def test_pvpc_prices_units(self, sm_mock: MagicMock):
        """Test the the values returned by
        `PricesManager.get_pvpc_prices` in different units.
        """
        # Mock
        sm_mock.return_value = SettingsManagerMock()

        pm = PricesManager()

        pvpc_k = pm.get_pvpc_prices("k")
        pvpc_m = pm.get_pvpc_prices("m")

        k_count = len(pvpc_k)
        m_count = len(pvpc_m)

        self.assertEqual(k_count, 24)
        self.assertEqual(m_count, 24)

        for i in range(k_count):
            act = pvpc_k[i]["value"]
            exp = round(pvpc_m[i]["value"] / 1000, 5)

            self.assertEqual(act, exp)
