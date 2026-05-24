### Requirements

- Python 3.10

### Create isolated virtual environment

```shell
python -m venv venv
```

### Start application

```shell
# Powershell
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app/main.py

# Cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
python app/main.py

# Linux / macOS (bash/zsh)
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

### Download yt-dlp.exe and ffmpeg.exe

1. https://github.com/yt-dlp/yt-dlp/releases
2. https://github.com/BtbN/FFmpeg-Builds/releases

### Free m3u8 streams

1. https://gist.github.com/Fazzani/8f89546e188f8086a46073dc5d4e2928
