import sys
from PyQt5.QtWidgets import QApplication
from comic_viewer import ComicViewer

def main():
    app = QApplication(sys.argv)
    viewer = ComicViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
