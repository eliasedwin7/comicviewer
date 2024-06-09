import time
import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QFileDialog, QAction,
                             QVBoxLayout, QWidget, QPushButton, QGridLayout,
                             QScrollArea, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDialogButtonBox)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import json

from PIL import Image

from comic_window import ComicWindow


def custom_sort(s):
    import re
    numbers = re.findall(r'\d+', s)
    # default to 0 if no number is found
    num = int(numbers[-1]) if numbers else 0
    return (num, s)


class ComicViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thumbnail_cache = {}
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        self.setWindowTitle("Comic Library")

        self.main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.grid_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.main_layout.addWidget(self.scroll_area)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Create the File menu and add actions to it
        file_menu = self.menuBar().addMenu("File")

        # Add an action to open a directory
        self.open_action = QAction("Open Directory", self)
        self.open_action.triggered.connect(self.open_directory)
        file_menu.addAction(self.open_action)

        # Add an action to connect to the network
        self.connect_action = QAction("Connect to Network", self)
        self.connect_action.triggered.connect(self.connect_to_network)
        file_menu.addAction(self.connect_action)

        # Add the search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.textChanged.connect(self.start_search_timer)
        self.main_layout.addWidget(self.search_bar)

        self.search_timer = QtCore.QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)

        self.date_opened = {}  # To keep track of when comics were opened
        self.all_files = {}
        # Load the file history
        self.load_history()

        # Open the last accessed directory if available
        self.open_last_directory()

    def start_search_timer(self):
        # Only start the timer if the query length is more than 2
        if len(self.search_bar.text()) > 2:
            self.search_timer.start(500)  # Increase delay to 500ms

    def load_history(self):
        try:
            with open('file_history.json', 'r') as f:
                loaded_history = json.load(f)
                # Ensure each value is a dictionary with at least the 'loaded' key
                self.file_history = {k: (v if isinstance(v, dict) else {
                                         "loaded": time.time(), "opened": {}}) for k, v in loaded_history.items()}
        except FileNotFoundError:
            self.file_history = {}

    def save_history(self):
        with open('file_history.json', 'w') as f:
            json.dump(self.file_history, f)

    def open_directory(self, mount_point=None):
        directory_path = mount_point if mount_point else QFileDialog.getExistingDirectory(
            self, "Open comic directory")

        if directory_path:
            # Save to history
            self.file_history[directory_path] = {
                "loaded": time.time(),
                "opened": {}
            }

            self.save_history()

            for root, _, files in os.walk(directory_path):
                comic_files = [file for file in files if file.lower().endswith(
                    ('.png', '.jpg', '.cvi'))]

                # Use the custom_sort function
                comic_files.sort(key=custom_sort)

                if comic_files:
                    group_name = os.path.basename(root)

                    # Check for parent directory and prepend its name
                    parent_name = os.path.basename(os.path.dirname(root))
                    if parent_name and parent_name != os.path.basename(directory_path):
                        group_name = parent_name + " - " + group_name

                    self.all_files[group_name] = [
                        os.path.join(root, file) for file in comic_files]

            self.display_comics()

    def perform_search(self):
        query = self.search_bar.text().lower()
        matching_comics = {k: v for k,
                           v in self.all_files.items() if query in k.lower()}

        # This line is for debugging
        print("Matching comics:", matching_comics.keys())

        # Clear the current comics display
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            widget.setParent(None)

        # Display only the matching comics
        self.display_comics(comics_to_display=matching_comics)

    def open_last_directory(self):
        if self.file_history:
            # Assuming the last item is the most recently added
            last_directory = list(self.file_history.keys())[-1]
            self.open_directory(mount_point=last_directory)

    def connect_to_network(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Connect to Network')

        layout = QFormLayout()

        # Fields for entering network share details
        network_path_edit = QLineEdit()
        username_edit = QLineEdit()
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.Password)

        layout.addRow('Network Path:', network_path_edit)
        layout.addRow('Username:', username_edit)
        layout.addRow('Password:', password_edit)

        # Buttons to confirm or cancel
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        dialog.setLayout(layout)

        # Show dialog and wait for user
        result = dialog.exec_()

        if result == QDialog.Accepted:
            network_path = network_path_edit.text()
            username = username_edit.text()
            password = password_edit.text()
            # Add your logic to connect to the network share here
            self.mount_drive(network_path, username, password)
            self.open_directory(mount_point=r'Z:')

    def mount_drive(self, network_path, username, password):
        mount_point = r'Z:'  # Or any unused drive letter
        network_path = r'\\192.168.0.1\USB_SanDisk32Gen1_1_3316\Milftoon_SiteRip_032021'
        username = 'admin'
        password = ''
        print(
            f'net use {mount_point} {network_path} /user:{username} {password}')
        subprocess.run(
            f'net use {mount_point} {network_path} /user:{username} {password}', shell=True)

    def display_comics(self, comics_to_display=None):
        if comics_to_display is None:
            comics_to_display = self.all_files
        # Clear the current comics display
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            widget.setParent(None)
        for index, (group_name, files) in enumerate(comics_to_display.items()):
            container = QWidget(self)
            layout = QVBoxLayout(container)

            layout.setAlignment(Qt.AlignTop)
            layout.setSpacing(5)
            layout.setContentsMargins(5, 5, 5, 5)

            thumbnail = QLabel(container)
            pixmap = QPixmap(files[0])
            scaled_pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio)
            thumbnail.setPixmap(scaled_pixmap)
            thumbnail.setFixedSize(scaled_pixmap.size())
            thumbnail.setToolTip(group_name)
            thumbnail.setFrameStyle(QLabel.Box)
            thumbnail.mousePressEvent = lambda event, files=files: self.view_comic(
                files)

            label = QLabel(group_name, container)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(150)

            # New Label for page count
            page_count_label = QLabel(f"{len(files)} pages", container)
            page_count_label.setAlignment(Qt.AlignCenter)
            page_count_label.setFixedWidth(150)

            layout.addWidget(thumbnail)
            layout.addWidget(label)
            # Add the page count label to the layout
            layout.addWidget(page_count_label)
            container.setLayout(layout)

            self.grid_layout.addWidget(container, index // 4, index % 4)
        # Update the layouts and central widget
        self.scroll_widget.setLayout(self.grid_layout)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def view_comic(self, files):
        self.comic_window = ComicWindow(files, self)
        self.comic_window.show()
        # self.comic_window.showFullScreen()

    def open_next_comic(self):
        current_comic_key = next((key for key, value in self.all_files.items(
        ) if value == self.comic_window.files), None)
        keys = list(self.all_files.keys())
        index = keys.index(current_comic_key)
        if index < len(keys) - 1:
            self.comic_window.close()
            self.view_comic(self.all_files[keys[index + 1]])

    def open_previous_comic(self):
        current_comic_key = next((key for key, value in self.all_files.items(
        ) if value == self.comic_window.files), None)
        keys = list(self.all_files.keys())
        index = keys.index(current_comic_key)
        if index > 0:
            self.comic_window.close()
            self.view_comic(self.all_files[keys[index - 1]])


class EnhancedComicViewer(ComicViewer):
    def __init__(self):
        super().__init__()
        # self.thumbnail_cache = {}  # For caching thumbnails
        # Add Options menu for sorting
        options_menu = self.menuBar().addMenu("Options")
        self.sort_menu = options_menu.addMenu("Sort by")

        self.sort_by_name_action = QAction("Name", self)
        self.sort_by_name_action.triggered.connect(self.sort_by_name)
        self.sort_menu.addAction(self.sort_by_name_action)

        self.sort_by_date_loaded_action = QAction("Date Loaded", self)
        self.sort_by_date_loaded_action.triggered.connect(
            self.sort_by_date_loaded)
        self.sort_menu.addAction(self.sort_by_date_loaded_action)

        self.sort_by_date_opened_action = QAction("Date Opened", self)
        self.sort_by_date_opened_action.triggered.connect(
            self.sort_by_date_opened)
        self.sort_menu.addAction(self.sort_by_date_opened_action)

    def load_history(self):
        try:
            with open('file_history.json', 'r') as f:
                self.file_history = json.load(f)
        except FileNotFoundError:
            self.file_history = {}

    def open_directory(self, mount_point=None):
        # directory_path = mount_point if mount_point else QFileDialog.getExistingDirectory(
        #     self, "Open comic directory")

        # if directory_path:
        #     self.file_history[directory_path] = {
        #         "loaded": time.time(),
        #         "opened": {}
        #     }
        #     self.save_history()
        super().open_directory(mount_point=mount_point)

    def view_comic(self, files):
        super().view_comic(files)
        current_comic_key = next(
            (key for key, value in self.all_files.items() if value == files), None)
        last_directory = list(self.file_history.keys())[-1]
        if "opened" not in self.file_history[last_directory]:
            self.file_history[last_directory]["opened"] = {}
        self.file_history[last_directory]["opened"][current_comic_key] = time.time()
        self.save_history()

    def display_comics(self, comics_to_display=None):
        if comics_to_display is None:
            comics_to_display = self.all_files

        # Explicitly clear the grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:  # Check if widget is not None
                widget.deleteLater()

        for index, (group_name, files) in enumerate(comics_to_display.items()):
            container = QWidget(self)
            layout = QVBoxLayout(container)
            layout.setAlignment(Qt.AlignTop)
            layout.setSpacing(5)
            layout.setContentsMargins(5, 5, 5, 5)

            thumbnail_path = files[0]
            if thumbnail_path in self.thumbnail_cache:
                scaled_pixmap = self.thumbnail_cache[thumbnail_path]
            else:
                pixmap = QPixmap(thumbnail_path)
                scaled_pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio)
                self.thumbnail_cache[thumbnail_path] = scaled_pixmap

            thumbnail = QLabel(container)
            thumbnail.setPixmap(scaled_pixmap)
            thumbnail.setFixedSize(scaled_pixmap.size())
            thumbnail.setToolTip(group_name)
            thumbnail.setFrameStyle(QLabel.Box)
            thumbnail.mousePressEvent = lambda event, files=files: self.view_comic(
                files)

            label = QLabel(group_name, container)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(150)

            page_count_label = QLabel(f"{len(files)} pages", container)
            page_count_label.setAlignment(Qt.AlignCenter)
            page_count_label.setFixedWidth(150)

            layout.addWidget(thumbnail)
            layout.addWidget(label)
            layout.addWidget(page_count_label)
            container.setLayout(layout)

            self.grid_layout.addWidget(container, index // 4, index % 4)

        self.scroll_widget.setLayout(self.grid_layout)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def sort_by_name(self):
        self.all_files = dict(
            sorted(self.all_files.items(), key=lambda item: item[0]))
        print(self.all_files)  # Debugging line
        self.display_comics()

        self.all_files = dict(
            sorted(self.all_files.items(), key=lambda item: item[0]))
        self.display_comics()

    def sort_by_date_loaded(self):
        def get_date_loaded(directory):
            item = self.file_history[directory]
            return item.get("loaded", 0) if isinstance(item, dict) else 0

        print("Before sorting:", self.all_files)  # Debugging line
        sorted_keys = sorted(
            self.file_history, key=get_date_loaded, reverse=True)
        self.all_files = {k: self.all_files[k]
                          for k in sorted_keys if k in self.all_files}
        print("After sorting:", self.all_files)  # Debugging line

        self.display_comics()
        self.update()

    def sort_by_date_opened(self):
        def most_recent_opened_time(directory):
            item = self.file_history[directory]
            if isinstance(item, dict) and "opened" in item:
                return max(item["opened"].values(), default=0)
            return 0

        sorted_keys = sorted(
            self.file_history, key=most_recent_opened_time, reverse=True)
        self.all_files = {k: self.all_files[k]
                          for k in sorted_keys if k in self.all_files}
        self.display_comics()
        self.update()


# Other methods remain similar


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     viewer = ComicViewer()
#     viewer.show()
#     sys.exit(app.exec_())
