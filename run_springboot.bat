@echo off
title Apex Institute ERP - Spring Boot Portal (Port 8082)
echo ============================================================
echo   STARTING SPRING BOOT COLLEGE STUDENT MANAGEMENT SYSTEM
echo   PORT: http://localhost:8082
echo ============================================================
echo.
echo Checking Java environment...
java -version
if %errorlevel% neq 0 (
    echo [ERROR] Java 17+ is not installed or not in PATH!
    pause
    exit /b
)

echo.
echo Select Database Mode:
echo   [1] MySQL Database (Default: student_db on localhost:3306)
echo   [2] H2 In-Memory Database (Zero-setup test mode, no MySQL needed)
echo.
set /p DB_CHOICE="Enter choice [1 or 2, default is 1]: "

if "%DB_CHOICE%"=="2" (
    echo.
    echo Launching Spring Boot with H2 database on http://localhost:8082 ...
    call .\mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=h2
) else (
    echo.
    echo Launching Spring Boot with MySQL database on http://localhost:8082 ...
    call .\mvnw.cmd spring-boot:run
)

pause
