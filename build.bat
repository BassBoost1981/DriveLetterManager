@echo off
REM Build-Skript für Drive Letter Manager
REM Erstellt eine portable .exe-Datei mit PyInstaller

echo ========================================
echo Drive Letter Manager - Build Script
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH verfügbar.
    echo Bitte installieren Sie Python von https://python.org
    pause
    exit /b 1
)

echo Python gefunden. Installiere PyInstaller...
pip install pyinstaller

echo.
echo Erstelle portable .exe-Datei...
echo.

REM PyInstaller-Befehl für portable .exe
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "DriveLetterManager" ^
    --icon=icon.ico ^
    --add-data "README.md;." ^
    --distpath "dist" ^
    --workpath "build" ^
    --specpath "build" ^
    drive_letter_manager.py

if errorlevel 1 (
    echo.
    echo FEHLER: Build fehlgeschlagen!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build erfolgreich abgeschlossen!
echo ========================================
echo.
echo Die portable .exe-Datei befindet sich in:
echo %CD%\dist\DriveLetterManager.exe
echo.
echo WICHTIG: Starten Sie die .exe als Administrator,
echo um Laufwerksbuchstaben ändern zu können.
echo.
pause
