#!/usr/bin/env python3
"""Generate FurrOS icons: FurrOS-coloured folders plus matching file types."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLACES = ROOT / "scalable" / "places"
MIMETYPES = ROOT / "scalable" / "mimetypes"
for d in (PLACES, MIMETYPES):
    d.mkdir(parents=True, exist_ok=True)

INK = "#0E080B"
PLUM = "#781C2C"
PAPER = "#FFECEC"
DIM = "#C8AAB4"

FOLDERS = {
    "folder": "#FF8CBE",
    "user-home": "#FFBE5A",
    "folder-documents": "#7FF0F0",
    "folder-download": "#78E6A0",
    "folder-music": "#FF8CBE",
    "folder-pictures": "#FFBE5A",
    "folder-videos": "#E23A44",
    "folder-templates": "#C8AAB4",
    "folder-publicshare": "#5FB4F0",
    "folder-desktop": "#FF8CBE",
    "folder-activities": "#FF8CBE",
    "folder-applications": "#7FF0F0",
    "folder-archives": "#FFBE5A",
    "folder-code": "#78E6A0",
    "folder-development": "#78E6A0",
    "folder-favorites": "#FF8CBE",
    "folder-games": "#E23A44",
    "folder-graphics": "#FFBE5A",
    "folder-network": "#5FB4F0",
    "folder-print": "#C8AAB4",
    "folder-system": "#E23A44",
    "folder-temp": "#781C2C",
}

FILES = {
    "text-x-generic": "#7FF0F0",
    "text-x-readme": "#FF8CBE",
    "text-x-script": "#78E6A0",
    "text-x-python": "#FFBE5A",
    "application-x-executable": "#78E6A0",
    "image-x-generic": "#FF8CBE",
    "audio-x-generic": "#78E6A0",
    "video-x-generic": "#FFBE5A",
    "application-pdf": "#E23A44",
    "package-x-generic": "#FFBE5A",
    "application-zip": "#781C2C",
    "x-office-document": "#5FB4F0",
    "x-office-spreadsheet": "#78E6A0",
    "x-office-presentation": "#FFBE5A",
    "text-css": "#5FB4F0",
    "text-html": "#E23A44",
    "text-x-changelog": "#C8AAB4",
    "application-json": "#FFBE5A",
    "application-x-shellscript": "#78E6A0",
}

BACK = (
    "M5 10 H18 L21 14 H42 A3 3 0 0 1 45 17 V39 "
    "A3 3 0 0 1 42 42 H5 A3 3 0 0 1 2 39 V13 A3 3 0 0 1 5 10 Z"
)
FRONT = "M2 21 H46 V39 A3 3 0 0 1 43 42 H5 A3 3 0 0 1 2 39 Z"
HIGHLIGHT = "M6 24 H20 V26 H6 Z"

PAW = f"""  <g fill="{PAPER}" opacity="0.30">
    <circle cx="29" cy="29" r="2.1"/>
    <circle cx="34" cy="27" r="2.4"/>
    <circle cx="39" cy="28" r="2.3"/>
    <circle cx="43" cy="31" r="2.0"/>
    <ellipse cx="36" cy="35" rx="6" ry="4" transform="rotate(-10 36 35)"/>
  </g>
"""


def lighten(hex_color: str, amount: float = 0.22) -> str:
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    channels = [round(c + (255 - c) * amount) for c in (r, g, b)]
    return "#" + "".join(f"{c:02X}" for c in channels)


def folder_svg(color: str, open_folder: bool = False) -> str:
    if open_folder:
        color = lighten(color)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <path d="{BACK}" transform="translate(3 3)" fill="{INK}" opacity="0.9"/>
  <path d="{BACK}" fill="{PLUM}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="{FRONT}" fill="{color}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="{HIGHLIGHT}" fill="{PAPER}" opacity="0.30"/>
{PAW}</svg>
"""


def file_svg(color: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <path d="M9 3 H29 L39 13 V43 A2 2 0 0 1 37 45 H9 A2 2 0 0 1 7 43 V5 A2 2 0 0 1 9 3 Z"
        transform="translate(3 3)" fill="{INK}" opacity="0.9"/>
  <path d="M9 3 H29 L39 13 V43 A2 2 0 0 1 37 45 H9 A2 2 0 0 1 7 43 V5 A2 2 0 0 1 9 3 Z"
        fill="{PAPER}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M29 3 V13 H39" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <rect x="11" y="6" width="15" height="6" rx="2" fill="{color}" stroke="{INK}" stroke-width="1.5"/>
  <rect x="12" y="21" width="22" height="3" rx="1.5" fill="{DIM}"/>
  <rect x="12" y="28" width="18" height="3" rx="1.5" fill="{DIM}"/>
  <rect x="12" y="35" width="21" height="3" rx="1.5" fill="{DIM}"/>
  <circle cx="33" cy="40" r="3" fill="{color}" stroke="{INK}" stroke-width="1.5"/>
</svg>
"""


def trash_svg() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <path d="M12 13 H36 L33 43 H15 Z" transform="translate(3 3)" fill="{INK}" opacity="0.9"/>
  <path d="M12 13 H36 L33 43 H15 Z" fill="#E23A44" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M9 10 H39" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
  <path d="M19 10 V6 H29 V10" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M20 20 V36 M24 20 V36 M28 20 V36" stroke="{PAPER}" stroke-width="2.5" stroke-linecap="round" opacity="0.75"/>
</svg>
"""


for name, color in FOLDERS.items():
    (PLACES / f"{name}.svg").write_text(folder_svg(color), encoding="utf-8")
    (PLACES / f"{name}-open.svg").write_text(
        folder_svg(color, open_folder=True), encoding="utf-8"
    )

for name, color in FILES.items():
    (MIMETYPES / f"{name}.svg").write_text(file_svg(color), encoding="utf-8")

(PLACES / "user-trash.svg").write_text(trash_svg(), encoding="utf-8")
(PLACES / "user-trash-full.svg").write_text(trash_svg(), encoding="utf-8")

print(
    f"Generated {len(FOLDERS) * 2 + len(FILES) + 2} icons "
    f"({PLACES}, {MIMETYPES})"
)
