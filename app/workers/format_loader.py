import subprocess
import os

from PySide6.QtCore import (
    QThread,
    Signal,
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class FormatLoaderThread(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            print(BASE_DIR)

            yt_dlp_path = os.path.join(
                BASE_DIR,
                "yt-dlp.exe",
            )

            result = subprocess.run(
                [yt_dlp_path, "-F", self.url],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            if result.returncode != 0:
                self.error.emit(result.stderr)
                return

            self.finished.emit(result.stdout)

        except Exception as e:
            self.error.emit(str(e))
