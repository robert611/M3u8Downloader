from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

def main():
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("M3U8 Downloader")
    window.resize(600, 400)

    layout = QVBoxLayout()

    label = QLabel("M3U8 Downloader")
    layout.addWidget(label)

    window.setLayout(layout)
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
