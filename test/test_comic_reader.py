from comic_viewer import ComicViewer
import pytest
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
sys.path.append('D:/Usefullpython/ComicViewer')


app = QApplication([])


@pytest.fixture
def viewer():
    return ComicViewer()


def test_initialization(viewer):
    """Test if the application initializes correctly."""
    assert viewer.windowTitle() == "Comic Library"


def test_open_directory(monkeypatch, viewer):
    """Test if comics are loaded properly from a directory."""
    # Mock the QFileDialog.getExistingDirectory to return a test directory path
    test_path = 'test/data/Archer-Armstrong-001'

    def mock_getExistingDirectory(*args, **kwargs):
        return test_path

    monkeypatch.setattr(QFileDialog, 'getExistingDirectory',
                        mock_getExistingDirectory)
    viewer.open_directory()
    assert viewer.all_files


def test_display_comics(qtbot, viewer):
    """Test the display_comics function."""
    viewer.all_files = {
        'TestComic1': ['data/Archer-Armstrong-001/Archer-Armstrong-001-01.jpg', 'data/Sirens_1/Sirens_1-08.jpg'],
        'TestComic2': ['data/Archer-Armstrong-001/Archer-Armstrong-001-12.jpg', 'data/Sirens_1/Sirens_1-09.jpg']
    }
    viewer.display_comics()

    # For simplicity, let's just check if the grid layout has the expected number of widgets.
    assert viewer.grid_layout.count() == len(viewer.all_files)


def test_view_comic(qtbot, viewer):
    """Test viewing a specific comic."""
    viewer.all_files = {
        'TestComic1': ['data/The_Eye_of_the_Dragon_-_Angelos_Kyprianos/The_Eye_of_the_Dragon_-_Angelos_Kyprianos-13.jpg', 'data/The_Eye_of_the_Dragon_-_Angelos_Kyprianos/The_Eye_of_the_Dragon_-_Angelos_Kyprianos-15.jpg']
    }
    viewer.view_comic(viewer.all_files['TestComic1'])

    # Check if the comic_window has been properly set up
    assert viewer.comic_window
    assert viewer.comic_window.files == viewer.all_files['TestComic1']

# More tests can be added, like testing navigation between comics and so on.
