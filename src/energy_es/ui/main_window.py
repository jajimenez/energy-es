"""Energy-ES - User Interface - Main Window."""

from os.path import join, dirname
from platform import uname

from tkinter import Tk, Menu, Image
from tkinter.messagebox import showinfo

from energy_es.ui.main_frame import MainFrame


class MainWindow(Tk):
    """Main window."""

    def __init__(self, *args, **kwargs):
        """Class initializer."""
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.on_quit)
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

            # File sub-menu
            self.file_menu = Menu(self.root_menu, tearoff=False)
            self.file_menu.add_command(label="Quit", command=self.on_quit)

            # Help sub-menu
            self.help_menu = Menu(self.root_menu, tearoff=False)
            self.help_menu.add_command(label="About", command=self.on_about)

            self.root_menu.add_cascade(menu=self.file_menu, label="File")
            self.root_menu.add_cascade(menu=self.help_menu, label="Help")

            self.configure(menu=self.root_menu)

    def on_quit(self):
        """Run logic when the Quit menu option is clicked."""
        self.destroy()
        self.quit()

    def on_about(self):
        """Run logic when the About menu option is clicked."""
        showinfo(
            title="About Energy-ES",
            message=(
                "Energy-ES\n"
                "Version 0.1.0\n"
                "Copyright © Jose A. Jimenez\n\n"
                "Data source: Red Eléctrica"
            )
        )

    def create_widgets(self):
        """Create the window widgets."""
        self.main_frame = MainFrame(self)
        self.main_frame.pack(expand=True, fill="both")
