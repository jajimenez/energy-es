"""Energy-ES - Tests - Data - Tools - Unit tests."""

from datetime import datetime
import unittest

# We import "paths" to include the "src" directory in "sys.path" so that we can
# import "userconf".
import paths

from energy_es.data.tools import get_time


class DataToolsTestCase(unittest.TestCase):
    """Unit tests of the "energy_es.data.tools" module."""

    def test_get_time(self):
        """Test the `energy_es.data.tools.get_time` function."""
        dt = datetime(2022, 12, 14, 14, 30)

        actual = get_time(dt)
        expected = "14:30"

        self.assertEqual(actual, expected)

        with self.assertRaises(AttributeError):
            get_time(None)
