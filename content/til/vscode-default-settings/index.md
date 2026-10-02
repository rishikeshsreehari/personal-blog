---
title: "VS Code Default Settings Are Read-Only"
date: 2026-08-25
tiltags: ["programming", "vscode", "troubleshooting"]
summary: "VS Code's Default Settings JSON is read-only. Custom changes go in User Settings or Workspace Settings instead."
url: "/til/vscode-default-settings-read-only"
---

Today I learned that the Settings JSON editor in VS Code has two files. The Default Settings file is read-only and can't be modified. If you want to customize anything, your changes need to go in User Settings (global) or Workspace Settings (per project).

For User Settings, open the Command Palette (`Ctrl+Shift+P`), search for "Preferences: Open Settings (JSON)" and add your overrides there.

For Workspace Settings (only applies to the current project), search for "Preferences: Open Workspace Settings (JSON)" instead.

Anything in either file takes priority over the defaults.