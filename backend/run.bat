@echo off
rem SAL Web - avvio manuale del server (doppio clic). I log sono visibili in questa finestra.
cd /d "%~dp0"
netstat -ano | findstr /R ":8000.*LISTEN" >nul && goto end
"..\.venv\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
:end
