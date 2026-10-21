@echo off
cd /d "%~dp0"
title VRAM Cleaner

if not exist "%~dp0vram_cleaner.pyw" (
    echo.
    echo  [Erreur] Fichier vram_cleaner.pyw introuvable.
    echo  Placez ce .bat dans le meme dossier que vram_cleaner.pyw
    echo.
    pause
    exit /b 1
)

where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" /B pythonw "%~dp0vram_cleaner.pyw"
    exit /b 0
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" /B python "%~dp0vram_cleaner.pyw"
    exit /b 0
)

echo.
echo  [Erreur] Python n'est pas installe ou n'est pas dans le PATH.
echo.
echo  1. Allez sur https://www.python.org/downloads/
echo  2. Installez Python
echo  3. Cochez la case "Add python.exe to PATH"
echo  4. Relancez ce fichier
echo.
pause
