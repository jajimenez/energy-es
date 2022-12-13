"""Energy-ES - User Interface - Main Window."""

from os.path import join, dirname

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView

from energy_es.ui.chart import get_chart_path


class MainWindow(QWidget):
    """Main window."""

    def __init__(self):
        """Class initializer."""
        super().__init__()

        self.setWindowTitle("Energy-ES")
        self.set_window_icon()
        self.resize(1000, 550)
        self.setMinimumSize(700, 400)

        self.create_widgets()

    def set_window_icon(self):
        """Set the window icon."""
        img_dir = join(dirname(__file__), "images")
        logo_path = join(img_dir, "logo.png")

        icon = QIcon(logo_path)
        self.setWindowIcon(icon)

    def create_widgets(self):
        """Create window widgets."""
        # Layout
        self._layout = QVBoxLayout(self)

        # Chart
        self._chart = QWebEngineView()
        self._layout.addWidget(self._chart)

        path = get_chart_path("k")  # Absolute path
        url = QUrl.fromLocalFile(path)
        self._chart.load(url)
