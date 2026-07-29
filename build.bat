@echo off
echo Cleaning old builds...
rmdir /s /q build dist

echo Building ChatBridge...
set PYTHONPATH=src
python -m PyInstaller --noconsole ^
            --name "ChatBridge" ^
            --icon "assets/icon.ico" ^
            --add-data "assets/icon.ico;assets" ^
            --paths src ^
            run.py

echo Build completed!
pause
