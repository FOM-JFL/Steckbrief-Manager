@echo off
title Steckbrief Manager - FOM
echo.
echo  ===================================
echo   Steckbrief Manager - FOM
echo   Version 6.0.0
echo  ===================================
echo.
echo  Starte lokalen Server auf Port 8080...
echo.
echo  Die App wird gleich im Browser geoeffnet.
echo  Dieses Fenster NICHT schliessen, solange die App laeuft!
echo.
timeout /t 2 /nobreak >nul
start "" "http://localhost:8080"
python -m http.server 8080
