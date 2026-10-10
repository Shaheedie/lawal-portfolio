@echo off
setlocal
cd /d "%~dp0"
echo.
echo   LNL Portfolio — Local Preview
echo   ----------------------------
where py >nul 2>nul
if %errorlevel%==0 (
  start "LNL Portfolio Server" cmd /k "cd /d ""%~dp0"" && py -m http.server 4173"
  goto open
)
where python >nul 2>nul
if %errorlevel%==0 (
  start "LNL Portfolio Server" cmd /k "cd /d ""%~dp0"" && python -m http.server 4173"
  goto open
)
echo Python was not found. Install Python or use the VS Code Live Server extension.
pause
exit /b 1
:open
timeout /t 2 /nobreak >nul
start "" "http://localhost:4173"
echo Preview opened. Keep the Portfolio Server window running.
exit /b 0
