import os
import re
import subprocess

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
)

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

        # layout
        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "EXT",
            "Rozdzielczość",
            "Rozmair",
            "Akcja",
        ])

        layout.addLayout(top_layout)
        layout.addWidget(self.error_box)
        layout.addWidget(QLabel("Dostępne formaty:"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def show_error(self, text):
        self.error_box.setText(text)
        self.error_box.show()

    def hide_error(self):
        self.error_box.hide()

    def load_formats(self):
        self.hide_error()

        url = self.url_input.text()

        if not url:
            self.show_error("Podaj URL")
            return

        try:
            yt_dlp_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "yt-dlp.exe",
            )

            result = subprocess.run(
                [yt_dlp_path, "-F", url],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            output = result.stdout

            self.table.setRowCount(0)

            for line in output.splitlines():

                if not re.match(r"^\d+", line):
                    continue

                parts = line.split()

                if len(parts) < 3:
                    continue

                format_id = parts[0]
                ext = parts[1]
                resolution = parts[2]

                if (parts[4] == '~'):
                    size = parts[5]
                else:
                    size = parts[4]

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

        except Exception as e:
            self.show_error(f"Błąd:\n{e}")

    def download_format(self, format_id):
        print(f"Pobieranie: {format_id}")
