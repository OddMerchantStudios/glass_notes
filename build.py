"""
Build script — compiles Glass Notes into a standalone .exe

Requirements:
    pip install pywebview pyinstaller

Run:
    py build.py

Output: dist/Glass Notes.exe
"""

import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(HERE, "icon.ico")
HTML = os.path.join(HERE, "app.html")

# Try finding PyInstaller executable directly first (handles multi-Python setups)
import shutil
pyinstaller_exe = shutil.which("pyinstaller") or shutil.which("pyinstaller.exe")

if pyinstaller_exe:
    cmd = [pyinstaller_exe,]
else:
    cmd = [sys.executable, "-m", "PyInstaller",]

cmd += [
    "--onefile",
    "--windowed",
    "--name", "Glass Notes",
    "--icon", ICON,
    "--clean",
    f"--add-data={HTML};.",
    f"--add-data={ICON};.",
    os.path.join(HERE, "main.py"),
]

print("Building Glass Notes.exe …")
result = subprocess.run(cmd)
if result.returncode == 0:
    print("\n✓ Done!  Find 'Glass Notes.exe' in the /dist folder.")
    print("  notes_data.json and notes_prefs.json will be saved next to the exe.")
else:
    print("\n✗ Build failed.")
    print("  Make sure you've run:  pip install pywebview pyinstaller")
