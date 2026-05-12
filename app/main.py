import subprocess
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
)

def on_download_clicked(url_input, output_box):
    print("Kliknięto przycisk")

    url = url_input.text()

    if not url:
        output_box.setText("Podaj URL")
        return

    try:
        yt_dlp_path = os.path.join(os.path.dirname(__file__), "yt-dlp.exe")

        result = subprocess.run(
            [yt_dlp_path, "-F", url],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        output_box.setPlainText(result.stdout)

    except Exception as e:
        output_box.setPlainText(f"Błąd:\n{e}")

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

    download_button = QPushButton("Pobierz")
    download_button.clicked.connect(
        lambda: on_download_clicked(url_input, output_box)
    )

    top_layout.addWidget(url_input)
    top_layout.addWidget(download_button)

    # Output
    output_box = QTextEdit()
    output_box.setReadOnly(True)

    layout.addLayout(top_layout)
    layout.addWidget(QLabel("Dostępne formaty:"))
    layout.addWidget(output_box)

    window.setLayout(layout)
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
