"""Energy-ES - User Interface - Main Window."""

from os.path import join, dirname

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox
)

from PySide6.QtWebEngineWidgets import QWebEngineView

from energy_es.ui.chart import get_chart_path


class MainWindow(QWidget):
    """Main window."""

    PRICE_UNITS = ["k", "m"]

    def __init__(self):
        """Class initializer."""
        super().__init__()

        self.setWindowTitle("Energy-ES")
        self.set_window_icon()
        self.resize(1020, 600)
        self.setMinimumSize(750, 450)

        self.create_widgets()

    def set_window_icon(self):
        """Set the window icon."""
        img_dir = join(dirname(__file__), "images")
        logo_path = join(img_dir, "logo.png")

        icon = QIcon(logo_path)
        self.setWindowIcon(icon)

    def create_widgets(self):
        """Create window widgets."""
        # Layout 1
        self._layout_1 = QVBoxLayout(self)

        # Chart
        self._chart = QWebEngineView(self)
        self._chart.setContextMenuPolicy(Qt.NoContextMenu)
        self._layout_1.addWidget(self._chart)
        self.update_chart("k")

        # Layout 2
        self._layout_2 = QHBoxLayout()
        self._layout_1.addLayout(self._layout_2)

        # Unit label
        self._unit_lab = QLabel(text="Prices unit:")

        self._layout_2.addWidget(
            self._unit_lab, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Unit combo box
        self._unit_combo = QComboBox()
        self._unit_combo.setFixedWidth(150)
        self._unit_combo.addItems(["€/KWh", "€/MWh"])
        self._unit_combo.currentIndexChanged.connect(self.on_unit_changed)

        self._layout_2.addWidget(
            self._unit_combo, stretch=True,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

    def update_chart(self, unit: str):
        """Update the chart widget.

        :param unit: Prices unit. It must be "k" to have the prices in €/KWh or
        "m" to have them in €/MWh.
        """
        path = get_chart_path(unit)  # Absolute path
        url = QUrl.fromLocalFile(path)
        self._chart.load(url)

    def on_unit_changed(self, x: int):
        """Run logic when the prices unit has changed.

        :param x: Selected unit index.
        """
        unit = MainWindow.PRICE_UNITS[x]
        self.update_chart(unit)
