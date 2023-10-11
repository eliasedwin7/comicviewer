import sys
from PyQt5.QtWidgets import QApplication
from comic_viewer import ComicViewer


from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QApplication, QMessageBox

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')

        self.username_label = QLabel('Username:')
        self.username_field = QLineEdit(self)

        self.password_label = QLabel('Password:')
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_credentials)

        layout = QVBoxLayout(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_field)
        layout.addWidget(self.login_button)

    def check_credentials(self):
        username = self.username_field.text()
        password = self.password_field.text()
        # Replace the following line with your authentication logic
        if username == 'admin' and password == 'password':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')


def main():
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()

    if login_dialog.exec_() == QDialog.Accepted:
        viewer = ComicViewer()  # Assuming ComicViewer is your main application window
        viewer.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()


