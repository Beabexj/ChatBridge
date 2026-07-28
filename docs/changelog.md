# Changelog

All notable changes to this project will be documented in this file.

## [v0.6.0] - 2026-07-29
### Added
- System Tray: ChatBridge now runs silently in the system tray with no console window.
- Left-click tray icon to toggle Enable/Disable translator.
- Right-click menu: Status toggle, Settings, Open Logs, About, Exit.
- Enable/Disable translator without restarting (hotkey still registered but silently skipped when disabled).
- `tray.py` module for all tray UI logic.
### Changed
- Refactored `src/` into proper `src/chatbridge/` Python package.
- `main.py` now spawns Hotkey Listener on a background daemon thread; `tray.run()` blocks the main thread.
- Clean shutdown: `keyboard.unhook_all()` + `sys.exit(0)` on Exit menu item.
### Updated
- `requirements.txt` now includes `pystray==0.19.5` and `pillow==12.3.0`.
- Version bumped to `0.6.0`.

## [v0.3.0] - 2026-07-29
### Added
- Config loader (config.py) and config.json to easily change hotkey and language targets without touching code.

## [v0.2.0] - 2026-07-29
### Changed
- Refactored architecture into `main.py`, `hotkey.py`, and `translator.py` following Single Responsibility Principle.

## [v0.1.0] - 2026-07-29
### Added
- Initial version. Press F8 to translate Thai -> English using Deep Translator and PyAutoGUI.
