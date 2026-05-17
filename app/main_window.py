import re

from PySide6.QtCore import (
    Qt,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QProgressBar,
)

from workers.download_worker import DownloadWorker
from workers.format_loader import FormatLoaderThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("M3u8 Downloader")
        self.resize(600, 400)

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()

        # Top layout
        top_layout = QHBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Wklej URL do m3u8...")

        self.load_button = QPushButton("Pokaż formaty")
        self.load_button.clicked.connect(
            lambda: self.load_formats()
        )

        top_layout.addWidget(self.url_input)
        top_layout.addWidget(self.load_button)

        # Success box
        self.success_box = QLabel()
        self.success_box.setStyleSheet("""
            background-color: #2b2b2b;
            color: #1f883d;
            border: 1px solid #444;
            padding: 5px;
        """)
        self.success_box.setWordWrap(True)
        self.success_box.hide()

        # Error box
        self.error_box = QLabel()
        self.error_box.setStyleSheet("""
            background-color: #2b2b2b;
            color: #ff5555;
            border: 1px solid #444;
            padding: 5px;
        """)
        self.error_box.setWordWrap(True)
        self.error_box.hide()

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        # layout
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "EXT",
            "Rozdzielczość",
            "Rozmiar",
            "Akcja",
        ])

        layout.addLayout(top_layout)
        layout.addWidget(self.error_box)
        layout.addWidget(self.success_box)
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("Dostępne formaty:"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def show_error(self, text):
        self.error_box.setText(text)
        self.error_box.show()

    def hide_error(self):
        self.error_box.hide()

    def load_formats(self):
        self.progress_bar.hide()
        self.hide_error()
        self.success_box.hide()

        url = self.url_input.text()

        if not url:
            self.show_error("Podaj URL")
            return

        self.load_button.setEnabled(False)

        self.thread = FormatLoaderThread(url)

        self.thread.finished.connect(
            self.on_formats_loaded
        )

        self.thread.error.connect(
            self.show_error
        )

        self.thread.finished.connect(
            lambda: self.load_button.setEnabled(True)
        )

        self.thread.start()

    def on_formats_loaded(self, output):
        self.table.setRowCount(0)

        resolutions_reached = False
        protocols = ["m3u8", "https", "http"]

        for line in output.splitlines():
            if not resolutions_reached:
                if "ID" in line and "EXT" in line:
                    resolutions_reached = True
                continue

            if not any(protocol in line for protocol in protocols):
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            format_id = parts[0]
            ext = parts[1]
            resolution = parts[2]
            size = self.extract_size(parts)

            row = self.table.rowCount()

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(format_id)
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(ext)
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(resolution)
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(size)
            )

            button = QPushButton("Pobierz")

            button.clicked.connect(
                lambda checked=False, f=format_id:
                self.download_format(f)
            )

            self.table.setCellWidget(
                row,
                4,
                button
            )

    def download_format(self, format_id):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.hide_error()
        self.success_box.hide()

        self.worker = DownloadWorker(
            self.url_input.text(),
            format_id
        )

        self.worker.progress.connect(
            self.progress_bar.setValue
        )

        self.worker.log.connect(
            lambda msg: print(msg)
        )

        self.worker.error.connect(self.show_error)

        self.worker.finished.connect(self.on_download_finished)

        self.worker.start()

        print(f"Pobieranie: {format_id}")

    def on_download_finished(self):
        self.success_box.setText("Pobieranie zakończone")
        self.success_box.show()

    def extract_size(self, parts):
        units = (
            "B", "KB", "MB", "GB", "TB",
            "KiB", "MiB", "GiB", "TiB",
        )

        for part in parts:
            cleaned = part.replace("~", "").strip()

            if any(unit in cleaned for unit in units):
                return cleaned

        return "Nieznany"
