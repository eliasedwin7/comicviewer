import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QFileDialog, QAction, 
                             QVBoxLayout, QWidget, QPushButton, QGridLayout, 
                             QScrollArea, QHBoxLayout,QDialog,QFormLayout,QLineEdit,QDialogButtonBox)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import json

from PIL import Image


def custom_sort(s):
    import re
    numbers = re.findall(r'\d+', s)
    num = int(numbers[-1]) if numbers else 0  # default to 0 if no number is found
    return (num, s)


class ComicViewer(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        self.all_files = {}
        # Load the file history
        self.load_history()

        # Open the last accessed directory if available
        self.open_last_directory()

    
    def load_history(self):
        try:
            with open('file_history.json', 'r') as f:
                self.file_history = json.load(f)
        except FileNotFoundError:
            self.file_history = {}
        
    def save_history(self):
        with open('file_history.json', 'w') as f:
            json.dump(self.file_history, f)

    def open_directory(self, mount_point=None):
        directory_path = mount_point if mount_point else QFileDialog.getExistingDirectory(self, "Open comic directory")
        
        if directory_path:
            # Save to history
            self.file_history[directory_path] = True
            self.save_history()
            
            for root, _, files in os.walk(directory_path):
                comic_files = [file for file in files if file.lower().endswith(('.png','.jpg'))]
                
                # Use the custom_sort function
                comic_files.sort(key=custom_sort)
                
                if comic_files:
                    group_name = os.path.basename(root)
                    self.all_files[group_name] = [os.path.join(root, file) for file in comic_files]
            
            self.display_comics()

    def open_last_directory(self):
        if self.file_history:
            last_directory = list(self.file_history.keys())[-1]  # Assuming the last item is the most recently added
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
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
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
        network_path=r'\\192.168.0.1\USB_SanDisk32Gen1_1_3316\Milftoon_SiteRip_032021'
        username='admin'
        password=''
        print(f'net use {mount_point} {network_path} /user:{username} {password}')
        subprocess.run(f'net use {mount_point} {network_path} /user:{username} {password}', shell=True)


        


    def display_comics(self):
        for index, (group_name, files) in enumerate(self.all_files.items()):
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
            thumbnail.mousePressEvent = lambda event, files=files: self.view_comic(files)
            
            label = QLabel(group_name, container)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(150)  
            
            # New Label for page count
            page_count_label = QLabel(f"{len(files)} pages", container)
            page_count_label.setAlignment(Qt.AlignCenter)
            page_count_label.setFixedWidth(150)
            
            layout.addWidget(thumbnail)
            layout.addWidget(label)
            layout.addWidget(page_count_label)  # Add the page count label to the layout
            container.setLayout(layout)
            
            self.grid_layout.addWidget(container, index // 4, index % 4)


    def view_comic(self, files):
        self.comic_window = ComicWindow(files, self)
        self.comic_window.show()

    def open_next_comic(self):
        current_comic_key = next((key for key, value in self.all_files.items() if value == self.comic_window.files), None)
        keys = list(self.all_files.keys())
        index = keys.index(current_comic_key)
        if index < len(keys) - 1:
            self.comic_window.close()
            self.view_comic(self.all_files[keys[index + 1]])

    def open_previous_comic(self):
        current_comic_key = next((key for key, value in self.all_files.items() if value == self.comic_window.files), None)
        keys = list(self.all_files.keys())
        index = keys.index(current_comic_key)
        if index > 0:
            self.comic_window.close()
            self.view_comic(self.all_files[keys[index - 1]])


class ComicWindow(QMainWindow):
    def __init__(self, files, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1000, 700)  # x, y, width, height
        self.parent = parent  # Keep a reference to the parent to access its methods
        self.setWindowTitle("Comic Viewer")

        self.layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.files = files

        self.setFocusPolicy(Qt.StrongFocus)
        self.installEventFilter(self)
        
        # Define the buttons and their handlers
        self.previous_page_button = QPushButton("Previous Page", self)
        self.previous_page_button.clicked.connect(self.previous_image)

        self.next_page_button = QPushButton("Next Page", self)
        self.next_page_button.clicked.connect(self.next_image)

        self.previous_comic_button = QPushButton("Previous Comic", self)
        self.previous_comic_button.clicked.connect(self.open_previous_comic)

        self.next_comic_button = QPushButton("Next Comic", self)
        self.next_comic_button.clicked.connect(self.open_next_comic)

        # Add buttons to a QHBoxLayout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.previous_page_button)
        self.button_layout.addWidget(self.next_page_button)
        self.button_layout.addWidget(self.previous_comic_button)
        self.button_layout.addWidget(self.next_comic_button)

        self.layout.addLayout(self.button_layout)  # Add button layout to the main layout
        self.current_index = 0
        # Load the first page
        self.load_image()
        # Show the window
        self.show()
        
    def eventFilter(self, obj, event):
        #print(QtCore.QEvent)  # Debugging line
        if event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
        return super().eventFilter(obj, event)

    
    def focusNextPrevChild(self, next_child):
        # Override to prevent focus change to child widgets (like buttons) when arrow keys are pressed
        return False
        

    def load_image(self):
        pixmap = QPixmap(self.files[self.current_index])
        self.image_label.setPixmap(pixmap.scaled(self.width() - 30, self.height() - 100, Qt.KeepAspectRatio))  # Add some margin for better fitting

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()

    def next_image(self):
        if self.current_index < len(self.files) - 1:
            self.current_index += 1
            self.load_image()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.next_image()
        elif event.key() == Qt.Key_Left:
            self.previous_image()
        elif event.key() == Qt.Key_Down:  # Navigate using down arrow for the next comic
            self.open_next_comic()
        elif event.key() == Qt.Key_Up:    # Navigate using up arrow for the previous comic
            self.open_previous_comic()

    def open_previous_comic(self):
        self.close()
        if self.parent:
            self.parent.open_previous_comic()
            
    def open_next_comic(self):
        self.close()
        if self.parent:
            self.parent.open_next_comic()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ComicViewer()
    viewer.show()
    sys.exit(app.exec_())
