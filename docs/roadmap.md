# ChatBridge Roadmap

## v0.1
- [x] F8 แปลข้อความ (เสร็จแล้ว)

## v0.2
- [x] แยกไฟล์ออกจาก main.py

## v0.3
- [x] config.json

## v0.4
- [x] Auto Detect Language

## v0.5
- [x] Refactor to `chatbridge` package

## v0.6
- [x] System Tray (Enable/Disable, Open Logs, About, Exit)

## v0.7
- [x] Settings UI (Tkinter)

## v0.8.0
- [x] Packaging (PyInstaller, resources.py, build.bat)

## v0.8.1
- [x] Fix Packaging Bugs (AppData Migration)

## v0.8.2
- [x] Polish EXE (Metadata, Version Info)

## v0.9 Beta (Quality & Usability)
- [x] v0.9.0 Performance Profiling & Latency Diagnostics
- [ ] Start with Windows
- [ ] Import / Export Settings
- [ ] Open Config Folder & Open Log Folder in UI
- [ ] Reset Settings
- [ ] Polish About Dialog
- [ ] Quality Assurance: Smoke Test, Memory Leak Test, Hotkey Stress Test, 8-hour continuous test

## v0.9.5 RC (Release Candidate)
- [ ] Complete Documentation (README, CHANGELOG, LICENSE, Release Notes)
- [ ] Add Screenshots
- [ ] Closed Alpha Testing (3-5 users)

## v1.0 Stable (Production Ready)
- [ ] Diagnostics & Health Check (Config, Logs, Network, Translator status)
- [ ] Tray Status Indicator (Yellow if degraded, Green if healthy)
- [ ] Crash Reporter (`crash.log` with traceback, OS version, etc.)
- [ ] Dogfooding Feedback Implementation (e.g., remember settings window position, ESC to cancel, hotkey conflicts)
- [ ] 0 Critical Bugs, VM tested, Build passes

## Post v1.0 Goals
- [ ] v1.1 Bug Fixes
- [ ] v1.2 Better UX
- [ ] v1.5 GitHub Actions + Auto Build
- [ ] v2.0 Plugin System
- [ ] v2.5 Multiple Translation Providers
- [ ] v3.0 Cross Platform (Windows/Linux)
