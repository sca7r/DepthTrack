# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-06-06

### Changed
- Refactored the monolithic `app.py` into an installable `depthtrack`
  package with clear `models`, `perception`, and `visualization` modules.
- Replaced runtime dependency auto-installation with `requirements.txt` and
  `pyproject.toml`.
- Replaced `print` logging with the standard `logging` module.
- Moved all magic numbers into a typed, validated configuration system
  (`config.py`) with YAML support and CLI overrides.

### Added
- Unit test suite (`pytest`) covering config, distance, risk, and rendering.
- `RiskLevel` enum for collision-risk levels.
- Dockerfile, Makefile, CI workflow, and contributor docs.
- A real CLI with `--config`, `--device`, `--conf`, `--output-dir`, and
  `--log-level` options plus `--version`.

### Fixed
- Corrected a misleading dependency comment that referenced a non-existent
  torch version.
- CUDA requests now cleanly fall back to CPU when unavailable.
