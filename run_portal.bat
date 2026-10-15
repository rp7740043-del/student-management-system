@echo off
title Apex Institute ERP - College Student Management System
echo ============================================================
echo   STARTING COLLEGE STUDENT MANAGEMENT SYSTEM (PORTAL)
echo ============================================================
echo.
echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    pause
    exit /b
)

echo.
echo Starting server on http://localhost:8082 ...
echo Default Credentials:
echo   - Admin: admin / admin123
echo   - Faculty: teacher / teacher123
echo.
python server.py
pause
