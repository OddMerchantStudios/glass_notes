# Glass Notes

A minimal sticky notes app for your desktop. Three note types — **notes**, **todos**, and **tallies** — on a clean, light canvas.

![Glass Notes demo](demo.gif)

---

## Features

- **Notes** — click to open and edit content
- **Todos** — click to check off
- **Tallies** — click to increment, displayed as `| |||| |||||`
- Right-click canvas to create a new note
- Click a title to rename it
- Right-click a tile for options (undo tally, mark undone, delete)
- Drag the canvas to move the window

---

## Run from source

**Requirements**
```
pip install pywebview
```

**Start the app**
```
python main.py
```

Your notes are saved to `notes_data.json` in the same folder.

---

## Build (Windows)

**Requirements**
```
pip install pywebview pyinstaller
```

**Build**
```
python build.py
```

Output: `dist/Glass Notes.exe` — fully self-contained, no install needed.

---

## Build on Mac / Linux

The app runs cross-platform via pywebview, but the build script uses Windows path separators (`;` in `--add-data`). To build on Mac or Linux, change the separator to `:` in `build.py`:

```python
# Change this:
f"--add-data={HTML};.",
f"--add-data={ICON};.",

# To this:
f"--add-data={HTML}:.",
f"--add-data={ICON}:.",
```

Then build normally:
```
python build.py
```

This will produce `dist/Glass Notes` (no `.exe`). The titlebar patching in `main.py` is Windows-only (Win32 API via ctypes) — on Mac you'll get a standard titlebar, which is fine. You can remove the `patch_window` call in `main.py` if you want a cleaner setup.

---
## Stack

- [pywebview](https://pywebview.flowrl.com/) — native window wrapping a WebView
- Vanilla HTML/CSS/JS — no frameworks
- PyInstaller — packaging
