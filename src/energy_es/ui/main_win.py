"""Energy-ES - User Interface - Main Window."""

from tkinter import Tk
from tkinter.ttk import Frame, Label

from energy_es.ui.chart import get_chart_widget


class MainFrame(Frame):
    """Main frame of the Main window."""

    def __init__(self, root=None):
        """Class initializer."""
        super().__init__(root)
        self.create_widgets()
        self.root = root

    def create_widgets(self):
        """Create the frame widgets."""
        self.chart, min_text, max_text = get_chart_widget(self)
        self.chart.pack(side="top", fill="x")

        self.summary = Frame(self)
        self.summary.pack(side="top", fill="x", padx=5, pady=5)

        self.min_lab_1 = Label(self.summary, text="Minimum price:")
        self.min_lab_1.grid(row=0, column=0, padx=(0, 5), sticky="w")

        self.min_lab_2 = Label(self.summary, text=min_text)
        self.min_lab_2.grid(row=0, column=1, sticky="w")

        self.max_lab_1 = Label(self.summary, text="Maximum price:")
        self.max_lab_1.grid(row=1, column=0, padx=(0, 5), sticky="w")

        self.max_lab_2 = Label(self.summary, text=max_text)
        self.max_lab_2.grid(row=1, column=1, sticky="w")


class MainWindow(Tk):
    """Main window."""

    def __init__(self, *args, **kwargs):
        """Class initializer."""
        super().__init__(*args, **kwargs)

        self.title("Energy-ES")
        self.set_geometry()
        self.create_widgets()

    def set_geometry(self):
        """Set the geometry (size and position) of the window."""
        # Screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Window size
        widget_width = 700
        widget_height = 480

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

    def create_widgets(self):
        """Create the window widgets."""
        self.main_frame = MainFrame(self)
        self.main_frame.pack(expand=True, fill="both")
