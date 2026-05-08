from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

def on_download_clicked():
    print("Kliknięto przycisk")
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
    download_button.clicked.connect(on_download_clicked)

    top_layout.addWidget(url_input)
    top_layout.addWidget(download_button)

    label = QLabel("M3U8 Downloader")

    layout.addLayout(top_layout)
    layout.addWidget(label)

    window.setLayout(layout)
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
