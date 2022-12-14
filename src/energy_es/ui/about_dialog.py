"""Energy-ES - User Interface - About Dialog."""

from os.path import join, dirname

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class AboutDialog(QDialog):
    """About dialog."""

    def __init__(self):
        """Class initializer."""
        super().__init__()

        self.setWindowTitle("About Energy-ES")
        self.setModal(True)
        self.setFixedSize(214, 278)

        self.create_widgets()

    def create_widgets(self):
        """Create window widgets."""
        # Layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # Logo label
        img_dir = join(dirname(__file__), "images")
        logo_path = join(img_dir, "logo.png")

        logo_pm = QPixmap(logo_path)
        logo_pm.scaled(100, 100, aspectMode=Qt.KeepAspectRatio)
        logo_pm.scaledToWidth(100)

        self._logo_lab = QLabel(pixmap=logo_pm)
        self._logo_lab.setFixedSize(100, 100)
        self._logo_lab.setScaledContents(True)

        self._layout.addWidget(self._logo_lab, alignment=Qt.AlignCenter)

        # Title label
        self._title_lab = QLabel(text="Energy-ES")

        font = self._title_lab.font()
        font.setBold(True)
        font.setPointSize(20)

        self._title_lab.setFont(font)
        self._layout.addWidget(self._title_lab, alignment=Qt.AlignCenter)

        # Version label
        self._version_lab = QLabel(text="Version 0.1.0")
        self._layout.addWidget(self._version_lab, alignment=Qt.AlignCenter)

        # Author label
        self._author_lab = QLabel(text="Copyright © Jose A. Jimenez")
        self._layout.addWidget(self._author_lab, alignment=Qt.AlignCenter)

        # License label
        self._license_lab = QLabel(text="MIT License")
        self._layout.addWidget(self._license_lab, alignment=Qt.AlignCenter)

        # Close button
        self._close_button = QPushButton(text="Close")
        self._close_button.clicked.connect(self.on_close)

        self._layout.addWidget(self._close_button, alignment=Qt.AlignRight)

    def on_close(self):
        """Run logic when the Close button is clicked."""
        self.close()