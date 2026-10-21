# Guide Inno Setup — créer l'installeur de VRAM Zero

Objectif : obtenir un seul fichier, `VRAM_Zero_Setup_2.0.exe`, qui installe VRAM Zero
(raccourcis, désinstallation, licence) sur n'importe quel PC Windows.

Durée : environ 10 minutes. Un script prêt à l'emploi est déjà fourni, vous n'avez rien à écrire.

---

## Avant de commencer

Vérifiez que le dossier contient bien :

- `dist\VRAM Zero\VRAM Zero.exe` et le dossier `_internal` à côté
- `assets\vram_zero.ico`
- `LICENSE`
- `installer\VRAM_Zero.iss` (le script)

> Si `dist\VRAM Zero\VRAM Zero.exe` est absent (supprimé par Avast), lancez `RECREER_EXE.bat`.
> **Ne déplacez pas** les dossiers : le script utilise des chemins relatifs.

---

## Méthode rapide (recommandée) : utiliser le script fourni

1. Ouvrez **Inno Setup Compiler** (menu Démarrer).
2. Menu **File → Open…** puis choisissez `installer\VRAM_Zero.iss`.
3. Appuyez sur **F9** (ou **Build → Compile**).
4. Attendez le message « Successful compile » dans la fenêtre du bas.
5. Votre installeur est dans `installer\Output\VRAM_Zero_Setup_2.0.exe`.

C'est tout. Passez à la section **Tester l'installeur**.

---

## Ce que fait le script (pour comprendre)

| Section | Rôle |
|---|---|
| `[Setup]` | Nom, version, éditeur, dossier d'installation (`Program Files\VRAM Zero`), licence, icône, nom du fichier final |
| `[Languages]` | Assistant d'installation en français |
| `[Tasks]` | Case « Créer une icône sur le Bureau » |
| `[Files]` | Copie tout `dist\VRAM Zero\` (EXE + `_internal`) dans le dossier d'installation |
| `[Icons]` | Raccourci dans le menu Démarrer, et sur le Bureau si la case est cochée |
| `[Run]` | Propose de lancer VRAM Zero à la fin de l'installation |

Ne modifiez **jamais** la ligne `AppId` : elle identifie le programme pour les mises à jour
et la désinstallation.

---

## Modifier les infos courantes

Tout se trouve en haut du fichier `.iss` :

```
#define AppVersion "2.0"       ← changez ici à chaque nouvelle version
#define AppPublisher "MEXAGORA"
```

Après modification : **F9** pour recompiler.

---

## Images de l'assistant (déjà faites et activées)

L'assistant d'installation affiche **deux** images :

- **L'image « large »** : le grand panneau vertical à **gauche** des pages de bienvenue et de fin
  (fichier `assets\wizard_large.bmp`, 164 × 314 px).
- **L'image « petite »** : le petit carré en **haut à droite** des pages intermédiaires
  (licence, dossier, installation) (fichier `assets\wizard_small.bmp`, 55 × 55 px).

Les deux sont déjà générées à partir de l'illustration pop-art, et le script les utilise
(lignes `WizardImageFile` et `WizardSmallImageFile`). **Vous n'avez rien à faire.**

Pour changer l'illustration : ouvrez le fichier .bmp dans Paint, collez votre image à la bonne taille,
enregistrez en **BMP** (pas en PNG ni en ICO) au même nom, puis **F9**.

---
## Tester l'installeur

1. Double-cliquez sur `installer\Output\VRAM_Zero_Setup_2.0.exe`.
2. Suivez l'assistant (licence → dossier → icône Bureau → installer).
3. Lancez VRAM Zero depuis le menu Démarrer : la fenêtre doit s'ouvrir avec son icône.
4. Testez la désinstallation : **Paramètres Windows → Applications → VRAM Zero → Désinstaller**.

Idéalement, testez sur un autre PC ou une machine virtuelle sans Python : c'est le vrai test.

---

## Problèmes fréquents

| Problème | Solution |
|---|---|
| « Source file not found » à la compilation | `dist\VRAM Zero\` est vide ou supprimé : lancez `RECREER_EXE.bat` |
| Avast ou Windows signale l'installeur | Faux positif fréquent avec les programmes Python. Ajoutez une exclusion, ou envoyez le fichier sur le site « Report false positive » de l'antivirus |
| Windows SmartScreen : « éditeur inconnu » | Normal sans certificat de signature de code. Cliquez sur **Informations complémentaires → Exécuter quand même** |
| L'application ne démarre pas après installation | Vérifiez que `_internal` a bien été installé à côté de `VRAM Zero.exe` |
| « nvidia-smi introuvable » dans l'application | Les pilotes NVIDIA ne sont pas installés sur ce PC : c'est normal sans carte NVIDIA |

---

## Publier une nouvelle version

1. Modifier `src\vram_zero.pyw` (changer `VERSION`).
2. Lancer `RECREER_EXE.bat`.
3. Changer `AppVersion` dans `installer\VRAM_Zero.iss`.
4. Ouvrir le `.iss` dans Inno Setup, puis **F9**.
5. Diffuser `installer\Output\VRAM_Zero_Setup_<version>.exe` (par exemple en « Release » sur GitHub).

