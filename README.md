# Dark MD Reader

A minimal, dark-themed desktop markdown viewer for Linux. Opens `.md` files and renders them beautifully in a warm dark theme that won't hurt your eyes — nothing more, nothing less.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop-41CD52?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)

## Features

- **Dark theme** — Catppuccin Mocha palette, easy on the eyes
- **GitHub-flavored Markdown** — headings, tables, lists, blockquotes, task lists, and more
- **Syntax-highlighted code blocks** — powered by Pygments (Monokai theme)
- **Find in page** — `Ctrl+F` with match count and navigation
- **Live reload** — auto-refreshes when the file changes on disk
- **Drag & drop** — drop a `.md` file onto the window to open it
- **Zero config** — single file, no build step, no settings to tweak

## Screenshot

<!-- Add a screenshot here: -->
<!-- ![screenshot](screenshot.png) -->

## Installation

### Prerequisites

Make sure you have the following installed (most Linux distros have these or can install them easily):

```bash
# Ubuntu / Debian
sudo apt install python3 python3-pyqt5 python3-pyqt5.qtwebengine python3-markdown python3-pygments

# Fedora
sudo dnf install python3 python3-qt5 python3-qt5-webengine python3-markdown python3-pygments

# Arch
sudo pacman -S python python-pyqt5 python-pyqt5-webengine python-markdown python-pygments
```

### Clone & Run

```bash
git clone https://github.com/alvi-uiu/dark-md-reader.git
cd dark-md-reader
python3 md_reader.py
```

## Usage

```bash
# Open a file directly
python3 md_reader.py README.md

# Launch empty, then use Ctrl+O to pick a file
python3 md_reader.py
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open a file |
| `Ctrl+F` | Find in page |
| `Ctrl+R` | Reload current file |
| `Ctrl+Q` | Quit |
| `Escape` | Close search bar |
| `Enter` | Next match (in search) |

### Set as Default App for `.md` Files

To open `.md` files with a double-click:

```bash
# Copy the desktop entry
cp md-reader.desktop ~/.local/share/applications/

# Set as default
xdg-mime default md-reader.desktop text/markdown
xdg-mime default md-reader.desktop text/x-markdown
```

## Project Structure

```
dark-md-reader/
├── md_reader.py          # The entire app (single file)
├── md-reader.desktop     # Linux desktop entry for app integration
├── LICENSE
└── README.md
```

## License

[MIT](LICENSE)
