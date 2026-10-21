@echo off
cd /d "%~dp0"
title VRAM Zero

if not exist "%~dp0src\vram_zero.pyw" (
    echo.
    echo  [Erreur] Fichier src\vram_zero.pyw introuvable.
    echo  Ne deplacez pas ce .bat hors du dossier VRAM_Zero.
    echo.
    pause
    exit /b 1
)

where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw "%~dp0src\vram_zero.pyw"
    exit /b 0
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" python "%~dp0src\vram_zero.pyw"
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
