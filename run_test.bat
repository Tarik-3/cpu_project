@echo off
echo Starting Flask server...
start /B python server.py
timeout /t 3 /nobreak >nul

echo.
echo Running test client...
python test.py

echo.
echo Press any key to stop the server...
pause >nul

taskkill /F /IM python.exe /FI "WINDOWTITLE eq server.py*" 2>nul
