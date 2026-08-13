#!/usr/bin/env python3
"""
Markdown Reader — A simple, dark-themed .md file viewer.

Usage:
    python3 md_reader.py                  # Opens empty, use File → Open
    python3 md_reader.py somefile.md      # Opens that file directly
"""

import sys
import os

from PyQt5.QtCore import Qt, QFileSystemWatcher, QSettings, QUrl
from PyQt5.QtGui import QKeySequence, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QShortcut,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWebEngineWidgets import QWebEnginePage

import markdown
from pygments.formatters import HtmlFormatter


# ---------------------------------------------------------------------------
# Dark theme CSS (Catppuccin Mocha inspired)
# ---------------------------------------------------------------------------

PYGMENTS_CSS = HtmlFormatter(style="monokai").get_style_defs(".codehilite")

DARK_CSS = """
* {
    box-sizing: border-box;
}

html {
    scrollbar-color: #45475a #1e1e2e;
}

body {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Noto Sans', 'Liberation Sans', Arial, sans-serif;
    font-size: 16px;
    line-height: 1.75;
    max-width: 860px;
    margin: 0 auto;
    padding: 40px 32px 80px 32px;
    -webkit-font-smoothing: antialiased;
}

/* ---- Headings ---- */
h1, h2, h3, h4, h5, h6 {
    color: #89b4fa;
    margin-top: 1.6em;
    margin-bottom: 0.5em;
    font-weight: 600;
    line-height: 1.3;
}

h1 {
    font-size: 2em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #313244;
}

h2 {
    font-size: 1.5em;
    padding-bottom: 0.25em;
    border-bottom: 1px solid #313244;
}

h3 { font-size: 1.25em; }
h4 { font-size: 1.1em; color: #b4befe; }
h5 { font-size: 1em; color: #b4befe; }
h6 { font-size: 0.9em; color: #a6adc8; }

/* ---- Paragraphs & text ---- */
p {
    margin: 0.8em 0;
}

strong {
    color: #f5e0dc;
    font-weight: 600;
}

em {
    color: #f5c2e7;
}

/* ---- Links ---- */
a {
    color: #89dceb;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
    color: #74c7ec;
}

/* ---- Horizontal rule ---- */
hr {
    border: none;
    border-top: 1px solid #313244;
    margin: 2em 0;
}

/* ---- Lists ---- */
ul, ol {
    padding-left: 1.8em;
    margin: 0.6em 0;
}

li {
    margin: 0.3em 0;
}

li > ul, li > ol {
    margin: 0.15em 0;
}

/* Task lists */
li input[type="checkbox"] {
    margin-right: 0.5em;
    accent-color: #89b4fa;
}

/* ---- Blockquotes ---- */
blockquote {
    border-left: 4px solid #45475a;
    background-color: #181825;
    margin: 1em 0;
    padding: 0.6em 1em;
    color: #a6adc8;
    border-radius: 0 6px 6px 0;
}

blockquote p {
    margin: 0.4em 0;
}

/* ---- Code ---- */
code {
    background-color: #181825;
    color: #a6e3a1;
    padding: 0.15em 0.4em;
    border-radius: 4px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
    font-size: 0.9em;
}

pre {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    margin: 1em 0;
}

pre code {
    background: none;
    padding: 0;
    color: #cdd6f4;
    font-size: 0.88em;
    line-height: 1.6;
}

/* Pygments code highlighting container */
.codehilite {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    margin: 1em 0;
}

.codehilite pre {
    background: none;
    border: none;
    padding: 0;
    margin: 0;
}

.codehilite code {
    background: none;
    padding: 0;
}

/* ---- Tables ---- */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.95em;
}

th {
    background-color: #313244;
    color: #89b4fa;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    border: 1px solid #45475a;
}

td {
    padding: 9px 14px;
    border: 1px solid #313244;
}

tr:nth-child(even) {
    background-color: #181825;
}

tr:nth-child(odd) {
    background-color: #1e1e2e;
}

tr:hover {
    background-color: #272738;
}

/* ---- Images ---- */
img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 1em 0;
}

/* ---- Definition lists ---- */
dt {
    font-weight: 600;
    color: #89b4fa;
    margin-top: 1em;
}

dd {
    margin-left: 1.5em;
    margin-bottom: 0.5em;
}

/* ---- Keyboard ---- */
kbd {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 4px;
    padding: 2px 6px;
    font-family: inherit;
    font-size: 0.85em;
    color: #cdd6f4;
    box-shadow: 0 1px 0 #45475a;
}

/* ---- Table of contents ---- */
.toc {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 1em 0;
}

.toc ul {
    list-style: none;
    padding-left: 1.2em;
}

.toc > ul {
    padding-left: 0;
}

.toc a {
    color: #89dceb;
}

/* ---- Selection ---- */
::selection {
    background-color: #45475a;
    color: #cdd6f4;
}

/* ---- Scrollbar (WebKit) ---- */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #1e1e2e;
}

::-webkit-scrollbar-thumb {
    background: #45475a;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #585b70;
}

/* ---- Empty state ---- */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    color: #585b70;
    text-align: center;
}

.empty-state .icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.empty-state p {
    font-size: 1.1em;
    margin: 0.3em 0;
}

.empty-state kbd {
    font-size: 0.85em;
}
"""

# Markdown extensions configuration
MD_EXTENSIONS = [
    "fenced_code",
    "codehilite",
    "tables",
    "toc",
    "nl2br",
    "sane_lists",
    "smarty",
    "attr_list",
    "def_list",
    "md_in_html",
]

MD_EXTENSION_CONFIGS = {
    "codehilite": {
        "css_class": "codehilite",
        "guess_lang": True,
        "linenums": False,
    },
    "toc": {
        "permalink": False,
    },
}

EMPTY_STATE_HTML = """
<div class="empty-state">
    <div class="icon">📄</div>
    <p>No file open</p>
    <p><kbd>Ctrl+O</kbd> to open a markdown file</p>
</div>
"""


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

APP_NAME = "Dark MD Reader"
ORG_NAME = "MdReader"
SETTINGS_GEOMETRY = "window/geometry"
SETTINGS_STATE = "window/state"
SETTINGS_LAST_DIR = "file/lastDir"


class MarkdownViewer(QMainWindow):
    """Main window for the Markdown Reader application."""

    def __init__(self, filepath=None):
        super().__init__()

        self.current_file = None
        self.watcher = QFileSystemWatcher(self)
        self.watcher.fileChanged.connect(self._on_file_changed)

        self._setup_ui()
        self._setup_shortcuts()
        self._restore_state()

        if filepath and os.path.isfile(filepath):
            self.open_file(filepath)
        else:
            self._show_empty_state()

    # -- UI setup ----------------------------------------------------------

    def _setup_ui(self):
        """Initialize the main UI components."""
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(700, 500)
        self.resize(900, 700)

        # No menu bar, no status bar
        self.menuBar().hide()
        self.setStatusBar(None)

        # Dark window background
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
        """)

        # Central widget with stacked layout for search overlay
        central = QWidget()
        central.setStyleSheet("background-color: #1e1e2e;")
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Search bar (hidden by default)
        self._setup_search_bar()
        layout.addWidget(self.search_bar)

        # Web view for rendering
        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        # Dark background for web view before content loads
        page = self.web_view.page()
        page.setBackgroundColor(QColor("#1e1e2e"))
        self.web_view.setStyleSheet("background-color: #1e1e2e;")

        # Settings — JavaScript enabled for find-in-page
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)

        layout.addWidget(self.web_view)
        self.setCentralWidget(central)

    def _setup_search_bar(self):
        """Create the Ctrl+F search bar widget."""
        self.search_bar = QWidget()
        self.search_bar.setFixedHeight(44)
        self.search_bar.setStyleSheet("""
            QWidget#searchBar {
                background-color: #181825;
                border-bottom: 1px solid #313244;
            }
            QLineEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
                selection-background-color: #45475a;
            }
            QLineEdit:focus {
                border-color: #45475a;
            }
            QPushButton {
                background-color: transparent;
                color: #a6adc8;
                border: none;
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #313244;
                color: #cdd6f4;
            }
            QLabel {
                color: #585b70;
                font-size: 12px;
            }
        """)
        self.search_bar.setObjectName("searchBar")

        bar_layout = QHBoxLayout(self.search_bar)
        bar_layout.setContentsMargins(12, 6, 12, 6)
        bar_layout.setSpacing(6)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find…")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._search_next)
        bar_layout.addWidget(self.search_input, 1)

        self.search_count_label = QLabel()
        bar_layout.addWidget(self.search_count_label)

        prev_btn = QPushButton("▲")
        prev_btn.setFixedSize(30, 28)
        prev_btn.setToolTip("Previous match (Shift+Enter)")
        prev_btn.clicked.connect(self._search_prev)
        bar_layout.addWidget(prev_btn)

        next_btn = QPushButton("▼")
        next_btn.setFixedSize(30, 28)
        next_btn.setToolTip("Next match (Enter)")
        next_btn.clicked.connect(self._search_next)
        bar_layout.addWidget(next_btn)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 28)
        close_btn.setToolTip("Close (Escape)")
        close_btn.clicked.connect(self._hide_search)
        bar_layout.addWidget(close_btn)

        self.search_bar.hide()

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self._open_dialog)
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self._reload_file)
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self._show_search)
        QShortcut(QKeySequence("Escape"), self, activated=self._hide_search)

    # -- Search operations -------------------------------------------------

    def _show_search(self):
        """Show the search bar and focus the input."""
        self.search_bar.show()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _hide_search(self):
        """Hide the search bar and clear highlights."""
        self.search_bar.hide()
        self.search_input.clear()
        self.search_count_label.clear()
        # Clear search highlights
        self.web_view.findText("")

    def _on_search_text_changed(self, text):
        """Triggered when search text changes — perform incremental search."""
        if text:
            self.web_view.findText(text, QWebEnginePage.FindFlags(), self._on_find_result)
        else:
            self.web_view.findText("")
            self.search_count_label.clear()

    def _search_next(self):
        """Find next match."""
        text = self.search_input.text()
        if text:
            self.web_view.findText(text, QWebEnginePage.FindFlags(), self._on_find_result)

    def _search_prev(self):
        """Find previous match."""
        text = self.search_input.text()
        if text:
            self.web_view.findText(text, QWebEnginePage.FindBackward, self._on_find_result)

    def _on_find_result(self, result):
        """Callback when find completes — update match count label."""
        if result.numberOfMatches() > 0:
            self.search_count_label.setText(
                f"{result.activeMatch()} / {result.numberOfMatches()}"
            )
            self.search_count_label.setStyleSheet("color: #585b70; font-size: 12px;")
        elif self.search_input.text():
            self.search_count_label.setText("No matches")
            self.search_count_label.setStyleSheet("color: #f38ba8; font-size: 12px;")
        else:
            self.search_count_label.clear()

    # -- File operations ---------------------------------------------------

    def _open_dialog(self):
        """Show file dialog to pick a markdown file."""
        settings = QSettings(ORG_NAME, APP_NAME)
        last_dir = settings.value(SETTINGS_LAST_DIR, os.path.expanduser("~"))

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            last_dir,
            "Markdown Files (*.md *.markdown *.mdown *.mkd *.mkdn *.txt);;All Files (*)",
        )

        if filepath:
            settings.setValue(SETTINGS_LAST_DIR, os.path.dirname(filepath))
            self.open_file(filepath)

    def open_file(self, filepath):
        """Open and render a markdown file."""
        filepath = os.path.abspath(filepath)

        if not os.path.isfile(filepath):
            return

        # Update watcher
        if self.current_file:
            self.watcher.removePath(self.current_file)

        self.current_file = filepath
        self.watcher.addPath(filepath)

        self._render()

    def _reload_file(self):
        """Reload the current file."""
        if self.current_file:
            self._render()

    def _on_file_changed(self, path):
        """Handle external file modifications."""
        # Some editors delete and recreate the file; re-add to watcher
        if not os.path.isfile(path):
            self.watcher.removePath(path)
            # Try to re-add after a brief moment (editor save race)
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(500, lambda: self._try_readd_watcher(path))
            return
        self._render()

    def _try_readd_watcher(self, path):
        """Attempt to re-add a path to the file watcher."""
        if os.path.isfile(path):
            self.watcher.addPath(path)
            self._render()

    # -- Rendering ---------------------------------------------------------

    def _render(self):
        """Read the current file, convert to HTML, and display."""
        if not self.current_file or not os.path.isfile(self.current_file):
            self._show_empty_state()
            return

        try:
            with open(self.current_file, "r", encoding="utf-8", errors="replace") as f:
                md_text = f.read()
        except Exception:
            return

        # Convert markdown to HTML
        md = markdown.Markdown(
            extensions=MD_EXTENSIONS,
            extension_configs=MD_EXTENSION_CONFIGS,
        )
        body_html = md.convert(md_text)

        # Build full HTML page
        html = self._build_html(body_html)

        # Use the file's directory as base URL so relative images work
        base_url = QUrl.fromLocalFile(os.path.dirname(self.current_file) + "/")
        self.web_view.setHtml(html, base_url)

        # Update title
        filename = os.path.basename(self.current_file)
        self.setWindowTitle(f"{filename} — {APP_NAME}")

    def _show_empty_state(self):
        """Show the empty/welcome state."""
        html = self._build_html(EMPTY_STATE_HTML)
        self.web_view.setHtml(html)
        self.setWindowTitle(APP_NAME)

    def _build_html(self, body_content):
        """Wrap body content in a full HTML page with dark CSS."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
{DARK_CSS}
{PYGMENTS_CSS}
    </style>
</head>
<body>
{body_content}
</body>
</html>"""

    # -- Window state persistence ------------------------------------------

    def _restore_state(self):
        """Restore window geometry from settings."""
        settings = QSettings(ORG_NAME, APP_NAME)
        geometry = settings.value(SETTINGS_GEOMETRY)
        state = settings.value(SETTINGS_STATE)
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)

    def closeEvent(self, event):
        """Save window geometry on close."""
        settings = QSettings(ORG_NAME, APP_NAME)
        settings.setValue(SETTINGS_GEOMETRY, self.saveGeometry())
        settings.setValue(SETTINGS_STATE, self.saveState())
        super().closeEvent(event)

    # -- Drag and drop -----------------------------------------------------

    def dragEnterEvent(self, event):
        """Accept drag events for files."""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    event.acceptProposedAction()
                    return

    def dropEvent(self, event):
        """Handle dropped files."""
        for url in event.mimeData().urls():
            if url.isLocalFile():
                filepath = url.toLocalFile()
                if os.path.isfile(filepath):
                    self.open_file(filepath)
                    break


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    # Handle high-DPI displays
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)

    # Check if a file was passed as argument
    filepath = None
    if len(sys.argv) > 1:
        candidate = sys.argv[1]
        if os.path.isfile(candidate):
            filepath = candidate
        else:
            print(f"Warning: '{candidate}' is not a valid file.", file=sys.stderr)

    viewer = MarkdownViewer(filepath)
    viewer.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
