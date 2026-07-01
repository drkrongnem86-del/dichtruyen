@echo off
chcp 65001 >nul 2>&1
echo ==============================================
echo   Build App Tinh Dich Truyen - PyInstaller
echo ==============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python!
    echo Download: https://www.python.org/downloads/
    echo Nho tick Add Python to PATH khi cai dat.
    pause
    exit /b 1
)

:: Install PyInstaller if missing
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing PyInstaller...
    pip install pyinstaller -q
    echo.
)

echo [*] Building .exe with PyInstaller...
echo.

:: Build with PyInstaller (use python -m to avoid PATH issues)
python -m PyInstaller ^
    --name "TinhDichTruyen" ^
    --onefile ^
    --windowed ^
    --clean ^
    main.py

echo.
if exist "dist\TinhDichTruyen.exe" (
    echo ==============================================
    echo   BUILD SUCCESS!
    echo   File: dist\TinhDichTruyen.exe
    echo ==============================================
) else (
    echo [ERROR] Build failed. Check errors above.
)

pause