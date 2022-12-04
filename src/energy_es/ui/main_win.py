"""Energy-ES - User Interface - Main Window."""

from tkinter import Tk
from tkinter.ttk import Frame, Label


class MainFrame(Frame):
    """Main frame of the Main window."""

    def __init__(self, root=None):
        """Class initializer."""
        super().__init__(root)
        self.create_widgets()

    def create_widgets(self):
        """Create the frame widgets."""
        self.title = Label(self, text="Energy prices in Spain")
        self.title.pack(side="top")


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
        widget_width = 320
        widget_height = 240

        # Border (space between window and widget) size
        border_width = self.winfo_rootx() - self.winfo_x()
        window_width = widget_width + (border_width * 2)

        border_height = self.winfo_rooty() - self.winfo_y()
        window_height = widget_height + (border_height * 2)

        # Center the window in the screen
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{widget_width}x{widget_height}+{x}+{y}")

    def create_widgets(self):
        """Create the window widgets."""
        self.main_frame = MainFrame(self)
        self.main_frame.pack(expand=True, fill="both")
