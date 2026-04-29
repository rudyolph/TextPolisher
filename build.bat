@echo off
echo Building TextPolisher Executable...

:: Ensure dependencies are installed
pip install -r requirements.txt

:: Run PyInstaller
:: --noconsole: No command prompt window when running
:: --onefile: Bundle everything into a single EXE
:: --clean: Clean cache before building
:: --name: Name of the output file
pyinstaller --noconsole --onefile --clean --name TextPolisher text_polisher.py

echo.
echo Build Complete! 
echo Your executable is in the "dist" folder.
echo.
echo IMPORTANT: Remember to copy "prompt.txt" and ".env" to the same folder as TextPolisher.exe!
pause
