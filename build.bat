@echo off
echo Cleaning old builds...
rmdir /s /q build dist

echo Building ChatBridge...
set PYTHONPATH=src
python -m PyInstaller --onefile --windowed ^
            --name "ChatBridge" ^
            --icon "assets/icon.ico" ^
            --version-file "assets/file_version_info.txt" ^
            --add-data "assets/icon.ico;assets" ^
            --paths src ^
            run.py

echo Build completed!
pause
