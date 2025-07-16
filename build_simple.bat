@echo off
echo Building Drive Letter Manager (Simple Version)...
echo.

REM Einfacher Build ohne erweiterte Optionen
pyinstaller --onefile --windowed --name DriveLetterManager drive_letter_manager.py

echo.
echo Build completed!
echo Executable can be found in: dist\DriveLetterManager.exe
pause
