@echo off
cd /d "%~dp0"
python -m pip install --quiet edge-tts
python jana_suara.py
echo.
echo Selesai! Fail 00.mp3 hingga 14.mp3 sudah dijana dalam folder ini.
pause
