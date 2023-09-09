from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QHBoxLayout, QScrollArea, QShortcut
)
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtCore import Qt, QSize

class ComicWindow(QMainWindow):
    def __init__(self, files, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1000, 700)
        self.parent = parent
        self.setWindowTitle("Comic Viewer")

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.zoom_level = 1  # Initial zoom level set to 1
        self.layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.image_label)

        # Add buttons to a QHBoxLayout
        self.button_layout = QHBoxLayout()

        self.previous_page_button = QPushButton("Previous Page", self)
        self.previous_page_button.clicked.connect(self.previous_image)

        self.next_page_button = QPushButton("Next Page", self)
        self.next_page_button.clicked.connect(self.next_image)

        self.previous_comic_button = QPushButton("Previous Comic", self)
        self.previous_comic_button.clicked.connect(self.open_previous_comic)

        self.next_comic_button = QPushButton("Next Comic", self)
        self.next_comic_button.clicked.connect(self.open_next_comic)

        self.button_layout.addWidget(self.previous_page_button)
        self.button_layout.addWidget(self.next_page_button)
        self.button_layout.addWidget(self.previous_comic_button)
        self.button_layout.addWidget(self.next_comic_button)

        self.layout.addLayout(self.button_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.scroll.setWidget(self.central_widget)
        self.setCentralWidget(self.scroll)

        self.files = files
        self.current_index = 0

        self.zoom_in_button = QPushButton("+", self)
        self.zoom_in_button.setFixedSize(QSize(50, 50))
        self.zoom_in_button.move(self.width() - 100, 0)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.zoom_out_button = QPushButton("-", self)
        self.zoom_out_button.setFixedSize(QSize(50, 50))
        self.zoom_out_button.move(self.width() - 50, 0)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        self.hide_buttons = False  # For toggling button visibility

        # Keyboard Shortcuts
        QShortcut(QKeySequence("Right"), self, self.next_image)
        QShortcut(QKeySequence("Left"), self, self.previous_image)
        QShortcut(QKeySequence("Up"), self, self.open_previous_comic)
        QShortcut(QKeySequence("Down"), self, self.open_next_comic)
        QShortcut(QKeySequence("+"), self, self.zoom_in)
        QShortcut(QKeySequence("-"), self, self.zoom_out)
        QShortcut(QKeySequence("H"), self, self.toggle_buttons)

        self.load_image()
        self.show()

    def load_image(self):
        pixmap = QPixmap(self.files[self.current_index])
        scaled_pixmap = pixmap.scaled(
            int(pixmap.width() * self.zoom_level),
            int(pixmap.height() * self.zoom_level),
            Qt.KeepAspectRatio
        )
        self.image_label.setPixmap(scaled_pixmap)

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()

    def next_image(self):
        if self.current_index < len(self.files) - 1:
            self.current_index += 1
            self.load_image()

    def open_previous_comic(self):
        self.close()
        if self.parent:
            self.parent.open_previous_comic()

    def open_next_comic(self):
        self.close()
        if self.parent:
            self.parent.open_next_comic()

    def zoom_in(self):
        self.zoom_level += 0.1
        self.load_image()

    def zoom_out(self):
        self.zoom_level -= 0.1
        self.load_image()

    def toggle_buttons(self):
        self.hide_buttons = not self.hide_buttons
        self.previous_page_button.setHidden(self.hide_buttons)
        self.next_page_button.setHidden(self.hide_buttons)
        self.previous_comic_button.setHidden(self.hide_buttons)
        self.next_comic_button.setHidden(self.hide_buttons)
        self.zoom_in_button.setHidden(self.hide_buttons)
        self.zoom_out_button.setHidden(self.hide_buttons)
