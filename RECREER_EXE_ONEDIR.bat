@echo off
title VRAM Cleaner - Reconstruction
cd /d "%~dp0"
echo.
echo  VRAM Cleaner — by CycleBlue
echo.

python -m pip install pyinstaller --upgrade >nul 2>&1

set ICON_OPT=
if exist "%~dp0vram_cleaner.ico" (
    set ICON_OPT=--icon="%~dp0vram_cleaner.ico"
    echo  Icone : vram_cleaner.ico
) else if exist "%~dp0icon.ico" (
    set ICON_OPT=--icon="%~dp0icon.ico"
    echo  Icone : icon.ico
) else (
    echo  [Info] Aucun .ico trouve. Placez vram_cleaner.ico ici puis relancez.
)

echo  Construction...
python -m PyInstaller --noconfirm --onedir --noconsole --name "VRAM Cleaner" %ICON_OPT% vram_cleaner.pyw
if errorlevel 1 (
    echo [Erreur] Echec.
    pause
    exit /b 1
)

if exist "%~dp0vram_cleaner.ico" copy /Y "%~dp0vram_cleaner.ico" "%~dp0dist\VRAM Cleaner\" >nul
if exist "%~dp0icon.ico" copy /Y "%~dp0icon.ico" "%~dp0dist\VRAM Cleaner\vram_cleaner.ico" >nul
if exist "%~dp0vram_cleaner.png" copy /Y "%~dp0vram_cleaner.png" "%~dp0dist\VRAM Cleaner\" >nul

echo.
echo  OK — dist\VRAM Cleaner\VRAM Cleaner.exe
echo.
pause
