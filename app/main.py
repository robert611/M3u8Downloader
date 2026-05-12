import subprocess
import re
import os

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

def load_formats(url_input, table, error_box):
    print("Kliknięto przycisk")

    error_box.hide()

    url = url_input.text()

    if not url:
        error_box.setText("Podaj URL")
        error_box.show()
        return

    try:
        yt_dlp_path = os.path.join(os.path.dirname(__file__), "yt-dlp.exe")

        result = subprocess.run(
            [yt_dlp_path, "-F", url],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        output = result.stdout

        table.setRowCount(0)

        for line in output.splitlines():

            # Pomijamy śmieci
            if not re.match(r"^\d+", line):
                continue

            parts = line.split()

            print(parts)

            if len(parts) < 3:
                continue

            format_id = parts[0]
            ext = parts[1]
            resolution = parts[2]

            print(format_id)
            print(ext)
            print(resolution)

            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, 0, QTableWidgetItem(format_id))
            table.setItem(row, 1, QTableWidgetItem(ext))
            table.setItem(row, 2, QTableWidgetItem(resolution))

            button = QPushButton("Pobierz")

            button.clicked.connect(
                lambda checked=False, f=format_id:
                download_format(f, url)
            )

            table.setCellWidget(row, 3, button)

    except Exception as e:
        error_box.setPlainText(f"Błąd:\n{e}")
        error_box.show()
        pass

    pass

def main():
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("M3U8 Downloader")
    window.resize(600, 400)

    layout = QVBoxLayout()

    top_layout = QHBoxLayout()

    url_input = QLineEdit()
    url_input.setPlaceholderText("Wklej URL do m3u8...")

    load_button = QPushButton("Pokaż formaty")

    top_layout.addWidget(url_input)
    top_layout.addWidget(load_button)

    # Error box
    error_box = QLabel()
    error_box.setStyleSheet("""
        background-color: #2b2b2b;
        color: #ff5555;
        border: 1px solid #444;
        padding: 5px;
    """)
    error_box.setWordWrap(True)
    error_box.hide()

    # Table
    table = QTableWidget()
    table.setColumnCount(4)

    table.setHorizontalHeaderLabels([
        "ID",
        "EXT",
        "Rozdzielczość",
        "Akcja"
    ])

    load_button.clicked.connect(
        lambda: load_formats(url_input, table, error_box)
    )

    layout.addLayout(top_layout)
    layout.addWidget(error_box)
    layout.addWidget(QLabel("Dostępne formaty:"))
    layout.addWidget(table)

    window.setLayout(layout)
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
