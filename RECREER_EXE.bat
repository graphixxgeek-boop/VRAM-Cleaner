@echo off
setlocal
cd /d "%~dp0"
title VRAM Zero - Reconstruction de l'EXE
echo.
echo  VRAM Zero - reconstruction de l'EXE (dist\VRAM Zero\VRAM Zero.exe)
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo  [Erreur] Python introuvable. Installez-le depuis https://www.python.org/downloads/
    echo  en cochant "Add python.exe to PATH", puis relancez ce fichier.
    if not defined CI pause
    exit /b 1
)

python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo  Installation de PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo  [Erreur] Impossible d'installer PyInstaller - connexion Internet requise.
        if not defined CI pause
        exit /b 1
    )
)

for %%F in (vram_zero.ico vram_zero_popart.png) do (
    if not exist "%~dp0assets\%%F" (
        echo  [Erreur] Fichier manquant : assets\%%F
        if not defined CI pause
        exit /b 1
    )
)

if exist "%~dp0dist\VRAM Zero" rmdir /s /q "%~dp0dist\VRAM Zero"

echo  Construction...
python -m PyInstaller --noconfirm --clean --onedir --noconsole ^
    --name "VRAM Zero" ^
    --icon "%~dp0assets\vram_zero.ico" ^
    --version-file "%~dp0assets\version_info.txt" ^
    --add-data "%~dp0assets\vram_zero.ico;." ^
    --add-data "%~dp0assets\vram_zero_popart.png;." ^
    --distpath "%~dp0dist" --workpath "%~dp0build" --specpath "%~dp0build" ^
    "%~dp0src\vram_zero.pyw"
if errorlevel 1 (
    echo.
    echo  [Erreur] Echec de la construction.
    if not defined CI pause
    exit /b 1
)

if exist "%~dp0build" rmdir /s /q "%~dp0build"

if not exist "%~dp0dist\VRAM Zero\VRAM Zero.exe" (
    echo.
    echo  [Attention] L'EXE a ete supprime juste apres sa creation :
    echo  c'est probablement Avast / l'antivirus. Ajoutez une exclusion sur ce dossier
    echo  puis relancez ce fichier.
    if not defined CI pause
    exit /b 1
)

echo.
echo  OK - dist\VRAM Zero\VRAM Zero.exe
echo.
if not defined CI pause
