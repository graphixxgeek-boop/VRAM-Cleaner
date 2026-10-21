# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Semantic Versioning](https://semver.org/).

## [2.0.0] - 2026-10-21

### Changed
- Project renamed from VRAM Cleaner to **VRAM Zero**.
- Source moved to `src/vram_zero.pyw`; icons and images moved to `assets/`.
- Process classification now compares executable names instead of loose substrings of the full path. Critical entries are checked before non-essential ones.

### Added
- Windows installer (Inno Setup script in `installer/`).
- Executable metadata (publisher, product, version).
- Automated build with GitHub Actions.
- Support for several NVIDIA GPUs (totals are summed).
- Illustration in the About window.

### Fixed
- Console windows flashing at each refresh.
- Selection lost on every refresh.
- Interface freezing while `nvidia-smi` runs (refresh now runs in the background).
- Duplicate refresh at startup and one redundant `nvidia-smi` call per cycle.
- Process names containing commas not being parsed.

## [1.3] - VRAM Cleaner

Initial public version.
