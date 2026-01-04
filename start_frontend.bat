@echo off
echo ============================================
echo   Opening Frontend in Browser
echo ============================================
echo.
echo Make sure the API server is running first!
echo Backend: http://localhost:8000
echo.
timeout /t 2 /nobreak > nul

REM Open index.html in default browser
start index.html

echo Frontend opened in your default browser.
echo.
pause
