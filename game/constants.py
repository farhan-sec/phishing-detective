"""
Shared constants for Phishing Detective.

Keeping colors/fonts in one place so the GUI file doesn't turn into
a swamp of hex codes. Tweak these if you want a different vibe.
"""

APP_TITLE = "Phishing Detective 🎣"
WINDOW_SIZE = "820x620"
MIN_WINDOW_SIZE = (720, 560)

# --- Colors ------------------------------------------------------------
BG_MAIN = "#f4f6fb"
BG_CARD = "#ffffff"
BG_HEADER = "#1c2541"

TEXT_DARK = "#1c1f26"
TEXT_MUTED = "#6b7280"
TEXT_LIGHT = "#f4f6fb"

ACCENT_BLUE = "#2f6fed"
ACCENT_BLUE_HOVER = "#255ac4"

GREEN = "#1fab55"
GREEN_HOVER = "#178a44"
GREEN_BG = "#e6f7ed"

RED = "#e14545"
RED_HOVER = "#c23434"
RED_BG = "#fdeaea"

GOLD = "#f5a623"

# --- Fonts ---------------------------------------------------------------
FONT_FAMILY = "Segoe UI"
MONO_FAMILY = "Consolas"

FONT_TITLE = (FONT_FAMILY, 22, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 11)
FONT_STATS = (FONT_FAMILY, 11, "bold")
FONT_LINK = (MONO_FAMILY, 15, "bold")
FONT_BUTTON = (FONT_FAMILY, 13, "bold")
FONT_FEEDBACK_TITLE = (FONT_FAMILY, 16, "bold")
FONT_FEEDBACK_BODY = (FONT_FAMILY, 11)
FONT_SMALL = (FONT_FAMILY, 9)

STARTING_LIVES = 3
