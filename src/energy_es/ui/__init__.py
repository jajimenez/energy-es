"""Energy-ES - User Interface."""

from energy_es.ui.main_win import MainWindow


def start_ui():
    """User interface main function.

    This function displays the main window.
    """
    win = MainWindow()
    win.mainloop()
