# Rapport VirusTotal — VRAM Zero.exe (application)

| Élément | Valeur |
|---|---|
| Référence (SHA-256) | `3093534e927045a14599225951df839507f7247a56d47c69443d9f35ade4d7be` |
| Lien du rapport | [https://www.virustotal.com/gui/file/3093534e927045a14599225951df839507f7247a56d47c69443d9f35ade4d7be](https://www.virustotal.com/gui/file/3093534e927045a14599225951df839507f7247a56d47c69443d9f35ade4d7be) |
| Fichier | VRAM Zero.exe |
| Taille | 1.86 MB (1953383 bytes) |
| Date d'analyse (UTC) | 2026-10-21 21:05:39 UTC |
| Résultat | 4 / 70 moteurs |
| Signature | File is not signed |

## Détections

| Moteur | Verdict |
|---|---|
| CrowdStrike Falcon | Win/malicious_confidence_60% (D) |
| SecureAge | Malicious |
| Skyhigh (SWG) | BehavesLike.Win64.Backdoor.tc |
| Zillya | Trojan.Blank.Script.2228 |

| Étiquette | Valeur |
|---|---|
| Étiquette de menace populaire | trojan.blank |
| Catégorie de menace | trojan |
| Famille | blank |

## Moteurs sans détection (66)

|  |  |  |  |
|---|---|---|---|
| Acronis (Static ML) | AhnLab-V3 | Alibaba | AliCloud |
| ALYac | Antiy-AVL | Arcabit | Arctic Wolf |
| Avast | AVG | Avira (no cloud) | BitDefender |
| Bkav Pro | ClamAV | CMC | CTX |
| Cynet | DeepInstinct | DrWeb | Elastic |
| Emsisoft | eScan | ESET-NOD32 | Fortinet |
| GData | Gridinsoft (no cloud) | Huorong | Ikarus |
| Jiangmin | K7AntiVirus | K7GW | Kaspersky |
| Kingsoft | Lionic | Malwarebytes | MaxSecure |
| McAfee Scanner | Microsoft | NANO-Antivirus | Palo Alto Networks |
| Panda | QuickHeal | Rising | Sangfor Engine Zero |
| SentinelOne (Static ML) | Sophos | SUPERAntiSpyware | Symantec |
| TACHYON | TEHTRIS | Tencent | Trapmine |
| Trellix ENS | TrendMicro | TrendMicro-HouseCall | Varist |
| VBA32 | VIPRE | VirIT | ViRobot |
| Webroot | WithSecure | Xcitium | Yandex |
| ZoneAlarm by Check Point | Zoner |  |  |

## Moteurs sans verdict

| Moteur | État |
|---|---|
| Avast-Mobile | Unable to process file type |
| BitDefenderFalx | Unable to process file type |
| Symantec Mobile Insight | Unable to process file type |
| Trustlook | Unable to process file type |
| Google | Aucun verdict |

## Empreintes

| Type | Valeur |
|---|---|
| MD5 | `d82c9e26ec9652acb5c9aeb829ba1409` |
| SHA-1 | `15335d50ed739092ad59e0944d873008dfee6542` |
| SHA-256 | `3093534e927045a14599225951df839507f7247a56d47c69443d9f35ade4d7be` |
| Vhash | `016076655d155d0575504013z3006emz2gz` |
| Authentihash | `315e00303cf45e504af10e90bd119637887b20a1fcf5e19a7ffe4855de46bf9a` |
| Imphash | `e3e80a143805ea18936c8f612e25d363` |
| Rich PE header hash | `a5ab84cd6b0f32306530937074b2749c` |
| SSDEEP | `24576:zvP5PHCEM85FNGERW3s9v9L+xUS4DJ94gnZ+DlwUTaFsA9PBCBk7xlc83iia3:bP5Kg5FN95d9H34gnZ+DlumoYui` |
| TLSH | `T1F0951258F3D894F1E4E3993D8EB28249D7B6B8110735C6CF0BA00B697E336E5293A751` |

## Type de fichier

| Élément | Valeur |
|---|---|
| Type | Win32 EXE, executable, windows, win32, pe, peexe |
| Magic | PE32+ executable (GUI) x86-64, for MS Windows |
| Taille | 1.86 MB (1953383 bytes) |

**TrID**

- Win64 Executable (generic) (37%)
- Win16 NE executable (generic) (28.6%)
- OS/2 Executable (generic) (11.5%)
- Generic Win/DOS Executable (11.3%)
- DOS Executable (generic) (11.3%)

**DetectItEasy**

- PE64
- Compiler: Microsoft Visual C/C++ (19.36.36246) [C]
- Linker: Microsoft Linker (14.36.36246)
- Tool: Visual Studio (2022 version 17.6)

## Historique

| Événement | Date (UTC) |
|---|---|
| Création | 2026-10-21 20:09:07 UTC |
| Première soumission | 2026-10-21 21:05:39 UTC |
| Dernière soumission | 2026-10-21 21:05:39 UTC |
| Dernière analyse | 2026-10-21 21:05:39 UTC |

## Noms

- VRAM Zero.exe
- VRAM Zero

## Signature

File is not signed

## Informations de version

| Champ | Valeur |
|---|---|
| Copyright | Copyright (c) 2026 MEXAGORA - Licence MIT |
| Produit | VRAM Zero |
| Description | VRAM Zero - Moniteur et liberation de la VRAM NVIDIA |
| Nom d'origine | VRAM Zero.exe |
| Nom interne | VRAM Zero |
| Version du fichier | 2.0.0.0 |

## Informations PE

**Produits du compilateur**

- [---] Unmarked objects count=163
- id: 0x105, version: 33145 count=189
- id: 0x104, version: 33145 count=12
- id: 0x103, version: 33145 count=11
- id: 0xfd, version: 35721 count=3
- id: 0x103, version: 35721 count=9
- id: 0x104, version: 35721 count=17
- id: 0x105, version: 35721 count=39
- id: 0x101, version: 33145 count=11
- id: 0x104, version: 36246 count=30

**En-tête**

| Champ | Valeur |
|---|---|
| Machine cible | x64 |
| Horodatage de compilation (UTC) | 2026-10-21 20:09:07 UTC |
| Point d'entrée | 59248 |
| Sections | 7 |

**Sections**

| Nom | Adresse virtuelle | Taille virtuelle | Taille brute | Entropie | MD5 | Chi2 |
|---|---|---|---|---|---|---|
| .text | 4096 | 204800 | 204800 | 6.49 | 5c1d0671232b92bd70fcd311921f85d8 | 1231419.75 |
| .rdata | 208896 | 84308 | 84480 | 5.7 | 2b806d54e0a12bdeddbe238b626e33c0 | 2546508.75 |
| .data | 294912 | 19192 | 3584 | 1.82 | 954eb046773252153f4899a4edd122ea | 589193.88 |
| .pdata | 315392 | 10092 | 10240 | 5.47 | 5bcb3226ba293f62cbcb0c82dfa00c46 | 299414.19 |
| .fptable | 327680 | 256 | 512 | 0 | bf619eac0cdf3f68d496ea9344137e8b | 130560 |

**Imports**

- USER32.dll
- COMCTL32.dll
- KERNEL32.dll
- ADVAPI32.dll
- GDI32.dll

**Ressources par type**

| Type | Nombre |
|---|---|
| RT_ICON | 6 |
| RT_MANIFEST | 1 |
| RT_VERSION | 1 |
| RT_GROUP_ICON | 1 |

**Ressources par langue**

| Langue | Nombre |
|---|---|
| NEUTRAL | 9 |

**Ressources contenues**

| SHA-256 | Type de fichier | Type | Langue | Entropie | Chi2 |
|---|---|---|---|---|---|
| `a049b36634b45e13ff975e0a87555ffe91cd78d5bd886a4d999fcb21ca29475b` | unknown | RT_ICON | NEUTRAL | 5.64 | 20290.19 |
| `bcf8f5884652b420b2ddeef625ccebc1ce75a17d545cf6b08d964be4839c5eb5` | unknown | RT_ICON | NEUTRAL | 5.67 | 84673.7 |
| `17a331a7897e76302d3d8fc6406aba322baaf335223e9abf23bdb1d018035113` | unknown | RT_ICON | NEUTRAL | 5.53 | 215293.97 |
| `e46b79421cbe7ba8f2c9a4951152dee6b62244eadb7564436b7079784dd31827` | unknown | RT_ICON | NEUTRAL | 5.51 | 390972.69 |
| `627005e97678671df5ccb0f33449524b91d52aff53c9b13ad87a0ca904b85523` | unknown | RT_ICON | NEUTRAL | 5.36 | 1797504.25 |

**Overlay**

| Champ | Valeur |
|---|---|
| chi2 | 1419.91 |
| filetype | unknown |
| entropy | 7.999291896820068 |
| offset | 501760 |
| size | 1451623 |
| md5 | `5f7fd885da7415a705540a8a0c64b894` |

