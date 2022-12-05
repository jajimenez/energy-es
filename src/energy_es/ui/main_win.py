"""Energy-ES - User Interface - Main Window."""

from os.path import join, dirname
from datetime import date
from platform import uname

from tkinter import Tk, Menu, Image, Event
from tkinter.messagebox import showinfo
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


class MainWindow(Tk):
    """Main window."""

    def __init__(self, *args, **kwargs):
        """Class initializer."""
        super().__init__(*args, **kwargs)

        self.title("Energy-ES")
        self.set_icon()
        self.set_geometry()
        self.create_menu()
        self.create_widgets()

    def set_icon(self):
        """Set the window icon.

        This function may work or not depending on the operating system.
        """
        img_dir = join(dirname(__file__), "images")
        logo_path = join(img_dir, "logo.png")

        try:
            img = Image("photo", file=logo_path)
            self.wm_iconphoto(True, img)
        except Exception:
            pass

    def set_geometry(self):
        """Set the geometry (size and position) of the window."""
        # Screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Window size
        widget_width = 700
        widget_height = 450

        # Border (space between window and widget) size
        border_width = self.winfo_rootx() - self.winfo_x()
        window_width = widget_width + (border_width * 2)

        border_height = self.winfo_rooty() - self.winfo_y()
        window_height = widget_height + (border_height * 2)

        # Center the window in the screen
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{widget_width}x{widget_height}+{x}+{y}")
        self.minsize(widget_width, widget_height)

    def create_menu(self):
        """Create the window menu."""
        plat = uname()[0].lower()

        if plat == "darwin":  # Mac OS
            self.tk.createcommand("tkAboutDialog", self.on_about)
            self.tk.createcommand("tk::mac::Quit", self.on_quit)
        else:  # Other OS
            self.root_menu = Menu()

            self.file_menu = Menu(self.root_menu, tearoff=False)
            self.file_menu.add_command(label="Quit", command=self.on_quit)

            self.help_menu = Menu(self.root_menu, tearoff=False)

            self.help_menu.add_command(
                label="About Energy-ES", command=self.on_about
            )

            self.root_menu.add_cascade(menu=self.file_menu, label="File")
            self.root_menu.add_cascade(menu=self.help_menu, label="Help")

            self.config(menu=self.root_menu)

    def on_quit(self):
        """Run logic when the Quit menu option is clicked."""
        self.quit()

    def on_about(self):
        """Run logic when the About menu option is clicked."""
        showinfo(
            title="About Energy-ES",
            message=(
                "Energy-ES\n"
                "Version 0.1.0\n"
                "Copyright \u00A9 Jose A. Jimenez\n\n"
                "Data source: Red Eléctrica"
            )
        )

    def create_widgets(self):
        """Create the window widgets."""
        self.main_frame = MainFrame(self)
        self.main_frame.pack(expand=True, fill="both")
