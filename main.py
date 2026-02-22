"""
Notes App — pywebview launcher
Install: pip install pywebview
Run:     py main.py
Build:   pip install pyinstaller && py build.py
"""

import webview
import json
import os
import sys
import threading

if getattr(sys, "frozen", False):
    BASE      = sys._MEIPASS
    DATA_FILE = os.path.join(os.path.dirname(sys.executable), "notes_data.json")
else:
    BASE      = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE, "notes_data.json")

HTML_FILE = os.path.join(BASE, "app.html")
_window   = None
_PREFS_FILE = os.path.join(os.path.dirname(DATA_FILE), "notes_prefs.json")


def load_prefs():
    try:
        with open(_PREFS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_prefs(prefs):
    try:
        with open(_PREFS_FILE, "w") as f:
            json.dump(prefs, f)
    except Exception:
        pass


def patch_window(hwnd):
    try:
        import ctypes, ctypes.wintypes

        user32  = ctypes.windll.user32
        dwmapi  = ctypes.windll.dwmapi

        # 1. Remove titlebar, keep thick resize border
        GWL_STYLE     = -16
        WS_CAPTION    = 0x00C00000
        WS_THICKFRAME = 0x00040000
        WS_SYSMENU    = 0x00080000
        style = user32.GetWindowLongW(hwnd, GWL_STYLE)
        style = (style & ~WS_CAPTION) | WS_THICKFRAME | WS_SYSMENU
        user32.SetWindowLongW(hwnd, GWL_STYLE, style)
        user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)

        # 2. Color the thin remaining border strip to match bg #1c1c1c
        # DWMWA_BORDER_COLOR = 34  (Windows 11 build 22000+)
        # Color is 0x00BBGGRR
        DWMWA_BORDER_COLOR = 34
        color = ctypes.c_uint(0x001c1c1c)  # #1c1c1c in BGR
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_BORDER_COLOR,
            ctypes.byref(color),
            ctypes.sizeof(color)
        )

        # 3. Also set caption color to match (hides any leftover caption strip)
        # DWMWA_CAPTION_COLOR = 35
        DWMWA_CAPTION_COLOR = 35
        cap_color = ctypes.c_uint(0x001c1c1c)
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_CAPTION_COLOR,
            ctypes.byref(cap_color),
            ctypes.sizeof(cap_color)
        )

    except Exception as e:
        print("patch_window error:", e)


def on_shown(window):
    try:
        import ctypes
        hwnd = None
        try:
            hwnd = window.get_native_handle()
        except Exception:
            pass
        if not hwnd:
            hwnd = ctypes.windll.user32.FindWindowW(None, "Glass Notes")
        if hwnd:
            patch_window(hwnd)
        else:
            print("Could not find HWND")
    except Exception as e:
        print("on_shown error:", e)


class Api:
    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"notes": []}

    def save(self, data):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print("Save error:", e)
            return False

    def move_to(self, x, y):
        """Move window to absolute screen position."""
        if _window:
            try:
                _window.move(int(x), int(y))
            except Exception as e:
                print("move_to error:", e)

    def save_size(self, w, h):
        try:
            save_prefs({"w": int(w), "h": int(h)})
        except Exception as e:
            print("save_size error:", e)

    def close_window(self):
        if _window:
            _window.destroy()


if __name__ == "__main__":
    api     = Api()
    prefs = load_prefs()
    win_w = prefs.get("w", 1100)
    win_h = prefs.get("h", 750)

    _window = webview.create_window(
        title="Glass Notes",
        url=f"file://{HTML_FILE}",
        js_api=api,
        width=win_w,
        height=win_h,
        min_size=(500, 400),
        background_color="#faf8f5",
        frameless=False,
        easy_drag=False,
    )

    def _patch():
        import time; time.sleep(0.3)
        on_shown(_window)

    _window.events.shown += lambda: threading.Thread(target=_patch, daemon=True).start()

    webview.start(debug=False)
