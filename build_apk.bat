@echo off
chcp 65001 >nul 2>&1
echo ==============================================
echo   Build APK Android - Tinh Dich Truyen
echo ==============================================
echo.

:: Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python!
    pause
    exit /b 1
)

:: Cài Kivy nếu chưa có
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing Kivy...
    pip install kivy -q
)

echo ==============================================
echo   CANH BAO QUAN TRONG:
echo   De build APK, can mo WSL hoac Linux:
echo ==============================================
echo.
echo   WSL Setup:
echo   1. wsl --install
echo   2. wsl
echo   3. Trong WSL, cai dat:
echo      sudo apt update
echo      sudo apt install -y python3 python3-pip openjdk-17-jdk
echo      pip install buildozer cython
echo.
echo   Build APK:
echo      cd /mnt/c/Users/MyPC/.mavis/sessions/mvs_743f10055b3a47f8bb9c47a9b011efbe/workspace
echo      buildozer -v android debug
echo.
echo   File APK se o: bin\tindichtruyen-1.0-debug.apk
echo ==============================================
echo.

:: Thử chạy thử trên desktop trước
echo [*] Neu muon test tren desktop, dang chay:
echo     python kivy_app.py
echo.

set /p choice="Ban co muon chay thu tren desktop khong? (y/n): "
if /i "%choice%"=="y" (
    python kivy_app.py
) else (
    echo Da len script. Hay lam theo huong dan WSL ben tren.
    pause
)