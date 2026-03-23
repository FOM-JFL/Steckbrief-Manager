@echo off
chcp 65001 >nul
title Steckbrief Manager (Prozesse ^& Projekte) - FOM (V15.1)
echo.
echo  ================================================
echo   Steckbrief Manager (Prozesse ^& Projekte) - FOM
echo   Version 15.1.0
echo  ================================================
echo.
echo  Pruefe Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  FEHLER: Python ist nicht installiert oder nicht im PATH.
    echo  Bitte Python 3.x installieren: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo  Pruefe benoetigte Python-Pakete...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo  Installiere Flask...
    pip install flask flask-cors >nul 2>&1
)
python -c "import mysql.connector" >nul 2>&1
if errorlevel 1 (
    echo  Installiere mysql-connector-python...
    pip install mysql-connector-python >nul 2>&1
)

echo.
echo  Starte API-Server (Port 5000) und Web-Server (Port 8080)...
echo  Die App wird gleich im Browser geoeffnet.
echo  Dieses Fenster NICHT schliessen, solange die App laeuft!
echo.

:: API-Server im Hintergrund starten
start "" /min cmd /c "title API-Server & python api_server.py"

:: Kurz warten, damit API bereit ist
timeout /t 2 /nobreak >nul

:: Browser oeffnen
start "" "http://localhost:8080"

:: HTTP-Server fuer Frontend starten (blockiert - haelt das Fenster offen)
python -m http.server 8080
