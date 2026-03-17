@echo off
REM Startet den lokalen Steckbrief-Manager auf Port 8080
cd /d "%~dp0"
python -m http.server 8080
pause