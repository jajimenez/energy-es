"""Energy-ES - User Interface - Main Window."""

from os.path import join, dirname

from PySide6.QtCore import Qt, QUrl, QObject, Signal, QThread
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox
)

from PySide6.QtWebEngineWidgets import QWebEngineView

from energy_es.ui.chart import get_message_html, get_chart_path


class ChartWorker(QObject):
    """Chart thread class.

    This class is used to generate the chart HTML file in a separate, parallel
    thread.
    """

    success = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self, unit: str):
        """Initialize the instance.

        :param unit: Prices unit. It must be "k" to have the prices in €/KWh or
        "m" to have them in €/MWh.
        """
        super().__init__()
        self._unit = unit

    def do_work(self):
        """Do the thread work.

        This method generates the chart HTML file in a separate, parallel
        thread and emits the file path or an error message HTML code if there
        is any error.
        """
        try:
            path = get_chart_path(self._unit)  # Absolute path
            self.success.emit(path)
        except Exception as e:
            title = "There was an error generating the chart"
            html = get_message_html(title, str(e))
            self.error.emit(html)
        finally:
            self.finished.emit()


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
        def on_success(path: str):
            url = QUrl.fromLocalFile(path)
            self._chart.load(url)

        def on_error(html: str):
            self._chart.setHtml(html)

        self.chart_thread = QThread()
        self.chart_worker = ChartWorker(unit)
        self.chart_worker.moveToThread(self.chart_thread)

        self.chart_thread.started.connect(self.chart_worker.do_work)
        self.chart_worker.finished.connect(self.chart_thread.quit)

        self.chart_worker.finished.connect(self.chart_worker.deleteLater)
        self.chart_thread.finished.connect(self.chart_thread.deleteLater)

        self.chart_worker.success.connect(on_success)
        self.chart_worker.error.connect(on_error)

        html = get_message_html("Generating the chart...")
        self._chart.setHtml(html)
        self.chart_thread.start()

    def on_unit_changed(self, x: int):
        """Run logic when the prices unit has changed.

        :param x: Selected unit index.
        """
        unit = MainWindow.PRICE_UNITS[x]
        self.update_chart(unit)
