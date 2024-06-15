# Comic Viewer

This repository contains two comic viewer applications: one built with PyQt5 and the other with Flask. Both applications allow users to upload, view, and segment comic images.

## Table of Contents

- [Comic Viewer](#comic-viewer)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [PyQt5 Application](#pyqt5-application)
    - [Flask Application](#flask-application)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Upload and view comic images.
- Segment comic pages into individual panels.
- Navigate between comics and panels.
- Zoom in and out on images.
- User authentication for the Flask application.

## Requirements

- Python 3.7+
- PyQt5
- Flask
- Pillow
- NumPy
- OpenCV

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/comic-viewer.git
   cd comic-viewer
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### PyQt5 Application

1. Navigate to the `pyqt5_viewer` directory:

   ```bash
   cd pyqt5_viewer
   ```

2. Run the PyQt5 comic viewer:

   ```bash
   python main.py
   ```

### Flask Application

1. Navigate to the `flask_viewer` directory:

   ```bash
   cd flask_viewer
   ```

2. Set the Flask environment variable:

   ```bash
   export FLASK_APP=app.py  # On Windows use `set FLASK_APP=app.py`
   ```

3. Run the Flask application:

   ```bash
   flask run
   ```

4. Open your browser and go to `http://127.0.0.1:5000`.

## Project Structure

```
comic-viewer/
│
├── pyqt5_viewer/
│   ├── main.py                  # Entry point for the PyQt5 application
│   ├── viewer.py                # PyQt5 main window and logic
│   └── ...                      # Other PyQt5 related files and resources
│
├── flask_viewer/
│   ├── app.py                   # Entry point for the Flask application
│   ├── segment_panels.py        # Segmentation logic
│   ├── templates/
│   │   ├── index.html           # Template for the home page
│   │   ├── login.html           # Template for the login page
│   │   ├── comic.html           # Template for viewing comics
│   │   └── ...                  # Other HTML templates
│   ├── static/
│   │   ├── uploads/             # Directory for uploaded comic images
│   │   └── ...                  # Other static files (CSS, JS, etc.)
│   └── ...                      # Other Flask related files and resources
│
├── requirements.txt             # Project dependencies
└── README.md                    # Project README file
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
