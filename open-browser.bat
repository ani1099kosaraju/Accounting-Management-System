@echo off
echo Opening Accounting Application in browser...
timeout /t 2 /nobreak >nul
start http://localhost:5000
echo.
echo If the application is not running, please run start.bat first!
pause
