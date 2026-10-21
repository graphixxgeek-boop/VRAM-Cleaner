# VRAM Zero v2.0 — by MEXAGORA

Surveillance et liberation de la VRAM NVIDIA (modeles IA locaux, applications gourmandes).

## Contenu du dossier

```
VRAM_Zero/
├── dist/VRAM Zero/            EXE pret a l'emploi (VRAM Zero.exe + _internal) -> a packager avec Inno Setup
├── src/vram_zero.pyw          Code source (Python 3, Tkinter, aucune dependance externe)
├── assets/
│   ├── vram_zero.ico          Icone de l'application (fenetre, EXE, installeur)
│   ├── vram_zero_popart.ico   Illustration pop-art (version ico)
│   └── vram_zero_popart.png   Illustration pop-art (affichee dans "A propos")
├── Lancer VRAM Zero.bat       Lance l'application depuis les sources (Python requis)
├── RECREER_EXE.bat            Reconstruit l'EXE dans dist\
├── installer/VRAM_Zero.iss    Script Inno Setup pret a compiler (voir GUIDE_INNO_SETUP.md)`r`n├── GUIDE_INNO_SETUP.md        Guide pas a pas pour creer l'installeur`r`n├── .github/workflows/build.yml  Compilation automatique (GitHub Actions)`r`n├── LICENSE                    Licence MIT`r`n├── GUIDE_PUBLICATION.md       Publication GitHub, antivirus, signature du code
└── README.md
```

## Lancer

- **EXE** : `dist\VRAM Zero\VRAM Zero.exe`
- **Sources** : double-clic sur `Lancer VRAM Zero.bat` (Python 3 dans le PATH)

## Reinstaller l'EXE (supprime ou mis en quarantaine par Avast ou un autre antivirus)

Double-cliquez sur **`RECREER_EXE.bat`**, ou depuis un terminal dans ce dossier :

```
RECREER_EXE.bat
```

Le script installe PyInstaller si besoin (Internet requis la premiere fois), reconstruit
`dist\VRAM Zero\VRAM Zero.exe` et signale si l'antivirus l'a supprime juste apres.

Si Avast le supprime a nouveau : ajoutez ce dossier aux **exclusions** d'Avast
(Menu > Parametres > General > Exceptions), puis relancez `RECREER_EXE.bat`.
Les faux positifs sont frequents avec les EXE crees par PyInstaller.

## Pour Inno Setup

- Dossier a embarquer : tout le contenu de `dist\VRAM Zero\` (EXE **et** `_internal`).
- Icone de l'installeur / du raccourci : `assets\vram_zero.ico`.
- Illustration pour l'assistant d'installation : `assets\vram_zero_popart.ico` / `.png`.
- Licence a afficher : `LICENSE`.

## Notes

- Necessite un GPU NVIDIA et `nvidia-smi` (installe avec les pilotes).
- Sous Windows, le pilote n'expose pas toujours la VRAM par processus (valeurs N/A) :
  les statistiques globales restent fiables.

## Licence

MIT — voir `LICENSE`.



