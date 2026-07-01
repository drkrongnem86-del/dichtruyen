@echo off
chcp 65001 >nul 2>&1
echo ==============================================
echo   Build APK qua Docker
echo ==============================================
echo.

:: Kiểm tra Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker chua cai dat!
    echo Download Docker Desktop: https://www.docker.com/products/docker-desktop/
    echo Sau khi cai, chay lai file nay.
    pause
    exit /b 1
)

echo [*] Build APK qua Docker...
echo.

:: Chạy Buildozer trong Docker container
docker run --rm ^
    -v "%CD%":/app ^
    -w /app ^
    --name buildozer ^
    kivy/buildozer:latest ^
    buildozer android debug 2>&1

echo.
if exist "bin\tindichtruyen-1.0-debug.apk" (
    echo ==============================================
    echo   BUILD THANH CONG!
    echo   File: bin\tindichtruyen-1.0-debug.apk
    echo ==============================================
) else (
    echo [ERROR] Build that bai. Kiem tra log ben tren.
)

pause