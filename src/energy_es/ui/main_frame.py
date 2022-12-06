"""Energy-ES - User Interface - Main Frame."""

from datetime import date

from tkinter import Event
from tkinter.ttk import Frame, Label, Combobox

from energy_es.data import PricesManager
from energy_es.ui.chart import get_chart_widget
from energy_es.ui.tools import get_time


class MainFrame(Frame):
    """Main frame of the Main window."""

    def __init__(self, root=None):
        """Class initializer."""
        super().__init__(root)

        self.root = root
        self.load_data()

    def load_data(self):
        """Load the data and create the frame widgets."""
        self._dt = date.today()

        try:
            pm = PricesManager()

            self._prices = pm.get_prices()
            self._min_price = min(self._prices, key=lambda x: x["value"])
            self._max_price = max(self._prices, key=lambda x: x["value"])

            self.create_widgets()
        except Exception:
            self.create_error_widgets()

    def create_widgets(self):
        """Create the frame widgets."""
        # Chart widget
        self.chart = get_chart_widget(self._prices, self)
        self.chart.pack(side="top", fill="x")

        # We need to reset the window icon as adding the chart sets the icon to
        # a Matplotlib icon.
        self.root.set_icon()

        # Summary widget
        self.summary = Frame(self)
        self.summary.pack(side="top", fill="x", padx=10, pady=5)

        # Minimum price widgets
        self.min_1 = Label(self.summary, text="Minimum price:")
        self.min_1.grid(row=0, column=0, sticky="w")

        min_hour = get_time(self._min_price["datetime"])
        min_value = self._min_price["value"]
        min_text = f"{min_hour}, {min_value} €/MWh"

        self.min_2 = Label(self.summary, text=min_text)
        self.min_2.grid(row=0, column=1, padx=(5, 0), sticky="w")

        # Maximum price widgets
        self.max_1 = Label(self.summary, text="Maximum price:")
        self.max_1.grid(row=1, column=0, sticky="w")

        max_hour = get_time(self._max_price["datetime"])
        max_value = self._max_price["value"]
        max_text = f"{max_hour}, {max_value} €/MWh"

        self.max_2 = Label(self.summary, text=max_text)
        self.max_2.grid(row=1, column=1, padx=(5, 0), sticky="w")

        # Widgets for the price by hour
        self.hour_1 = Label(self.summary, text="Price by hour:")

        self.hour_1.grid(
            row=2, column=0, columnspan=2, pady=(10, 0), sticky="w"
        )

        hours_values = [get_time(i["datetime"]) for i in self._prices]

        self.hours = Combobox(
            self.summary, state="readonly", values=hours_values, width=10
        )

        self.hours.bind("<<ComboboxSelected>>", self.on_hour_selected)
        self.hours.grid(row=3, column=0, sticky="w")

        self.hour_2 = Label(self.summary, text="")
        self.hour_2.grid(row=3, column=1, padx=(5, 0), sticky="w")

        # Select first hour. Calling the "set" method of a combo box widget
        # doesn't trigger the "<<ComboboxSelected>>" event and, therefore, we
        # need to call the "select_hour" method of this class.
        f = hours_values[0]

        self.hours.set(f)
        self.select_hour(f)

    def create_error_widgets(self):
        """Create the widgets of the frame when an error happened."""
        self.error = Label(self, text="There was an error getting the data")
        self.error.pack(side="top", fill="x", padx=10, pady=10)

    def on_hour_selected(self, event: Event):
        """Run logic when an hour string ("HH:MM") is selected.

        :param event: Event object.
        """
        hour = self.hours.get()  # Selected hour in the combo box
        self.select_hour(hour)

    def select_hour(self, hour: str):
        """Select an hour.

        :param: Hour string ("HH:MM").
        """
        # Get the price for the selected hour
        i = self.hours["values"].index(hour)
        value = self._prices[i]["value"]

        # Update label
        text = f"{value} €/MWh"
        self.hour_2.configure(text=text)
