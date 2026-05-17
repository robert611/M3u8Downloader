import os
import subprocess
import re

from PySide6.QtCore import (
    QThread,
    Signal,
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class DownloadWorker(QThread):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url, format_id):
        super().__init__()
        self.url = url
        self.format_id = format_id

    def run(self):
        try:
            yt_dlp_path = os.path.join(
                BASE_DIR,
                "yt-dlp.exe"
            )

            process = subprocess.Popen(
                [
                    yt_dlp_path,
                    "-f", f"{self.format_id}+bestaudio/{self.format_id}",
                    "--no-playlist",
                    "--downloader", "ffmpeg",
                    "--hls-use-mpegts",
                    "--ffmpeg-location", "ffmpeg.exe",
                    "--newline",
                    self.url,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )

            duration = None

            while True:
                line = process.stderr.readline()

                if not line:
                    break

                self.log.emit(line.strip())

                # duration
                duration_match = re.search(r"Duration:\s(\d+:\d+:\d+\.\d+)", line)
                if duration_match:
                    duration = self.time_to_seconds(duration_match.group(1))

                # progress (time-based)
                time_match = re.search(r"time=(\d+:\d+:\d+\.\d+)", line)
                if time_match and duration:
                    current = self.time_to_seconds(time_match.group(1))
                    percent = (current / duration) * 100
                    self.progress.emit(int(percent))

            process.wait()

            if process.returncode != 0:
                self.error.emit("Download failed")
                return

            self.progress.emit(100)
            self.finished.emit('done')

        except Exception as e:
            self.error.emit(str(e))

    def time_to_seconds(self, t):
        h, m, s = t.split(":")
        return int(h)*3600 + int(m)*60 + float(s)
