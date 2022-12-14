"""Energy-ES - User Interface - About Dialog."""

from os.path import join, dirname

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel


class AboutDialog(QDialog):
    """About dialog."""

    def __init__(self):
        """Class initializer."""
        super().__init__()

        self.setWindowTitle("About Energy-ES")
        self.setModal(True)
        self.create_widgets()

    def create_widgets(self):
        """Create window widgets."""
        # Layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # Logo
        img_dir = join(dirname(__file__), "images")
        logo_path = join(img_dir, "logo.png")

        # Title label
        self._title_lab = QLabel(text="Energy-ES 0.1.0")
        self._layout.addWidget(self._title_lab)

        # Author label
        self._author_lab = QLabel(text="Copyright © Jose A. Jimenez")
        self._layout.addWidget(self._author_lab)
