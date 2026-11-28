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

# Folder colour, plus an optional glyph drawn on a large paper sticker.
FOLDERS = {
    "folder": ("#FF8CBE", None),
    "user-home": ("#FFBE5A", "home"),
    "folder-documents": ("#7FF0F0", "doc"),
    "folder-download": ("#78E6A0", "download"),
    "folder-music": ("#FF8CBE", "note"),
    "folder-pictures": ("#FFBE5A", "image"),
    "folder-videos": ("#E23A44", "film"),
    "folder-templates": ("#C8AAB4", "plus"),
    "folder-publicshare": ("#5FB4F0", "share"),
    "folder-desktop": ("#FF8CBE", "monitor"),
    "folder-activities": ("#FF8CBE", None),
    "folder-applications": ("#7FF0F0", "grid4"),
    "folder-archives": ("#FFBE5A", "zip"),
    "folder-code": ("#78E6A0", "code"),
    "folder-development": ("#78E6A0", "code"),
    "folder-favorites": ("#FF8CBE", "star"),
    "folder-games": ("#E23A44", "gamepad"),
    "folder-graphics": ("#FFBE5A", "image"),
    "folder-network": ("#5FB4F0", "globe"),
    "folder-print": ("#C8AAB4", "printer"),
    "folder-system": ("#E23A44", "gear"),
    "folder-temp": ("#781C2C", "clock"),
    "folder-downloads": ("#78E6A0", "download"),
    "folder-video": ("#E23A44", "film"),
    "folder-photo": ("#FFBE5A", "image"),
    "folder-work": ("#C8AAB4", "grid4"),
    "folder-cloud": ("#5FB4F0", "globe"),
    "folder-remote": ("#5FB4F0", "globe"),
    "folder-recent": ("#C8AAB4", "clock"),
    "folder-bookmarks": ("#FF8CBE", "star"),
    "folder-saved-search": ("#FFBE5A", "star"),
    "folder-dropbox": ("#5FB4F0", "share"),
    "folder-onedrive": ("#5FB4F0", "globe"),
    "folder-google-drive": ("#FFBE5A", "share"),
    "folder-private": ("#781C2C", "gear"),
}

# File colour, glyph, optional short label in the coloured header strip.
FILES = {
    "text-x-generic": ("#7FF0F0", "lines", None),
    "text-plain": ("#7FF0F0", "lines", None),
    "text-x-readme": ("#FF8CBE", "readme", None),
    "text-x-changelog": ("#C8AAB4", "changelog", None),
    "text-x-script": ("#78E6A0", "shell", None),
    "application-x-shellscript": ("#78E6A0", "shell", None),
    "text-x-python": ("#FFBE5A", "code", "PY"),
    "text-x-c": ("#5FB4F0", "code", "C"),
    "text-x-c++": ("#5FB4F0", "code", "C++"),
    "text-x-java": ("#E23A44", "code", "JAVA"),
    "text-x-rust": ("#FF8CBE", "code", "RS"),
    "text-x-go": ("#7FF0F0", "code", "GO"),
    "application-javascript": ("#FFBE5A", "code", "JS"),
    "application-json": ("#FFBE5A", "braces", "JSON"),
    "application-xml": ("#7FF0F0", "code", "XML"),
    "application-x-yaml": ("#78E6A0", "code", "YML"),
    "text-css": ("#5FB4F0", "hash", "CSS"),
    "text-html": ("#E23A44", "code", "HTML"),
    "application-x-executable": ("#78E6A0", "exec", None),
    "application-pdf": ("#E23A44", "lines", "PDF"),
    "image-x-generic": ("#FF8CBE", "image", None),
    "image-png": ("#FF8CBE", "image", "PNG"),
    "image-jpeg": ("#FF8CBE", "image", "JPG"),
    "image-svg+xml": ("#FFBE5A", "image", "SVG"),
    "audio-x-generic": ("#78E6A0", "note", None),
    "audio-mpeg": ("#78E6A0", "note", "MP3"),
    "video-x-generic": ("#FFBE5A", "play", None),
    "video-mp4": ("#FFBE5A", "play", "MP4"),
    "x-office-document": ("#5FB4F0", "lines", "DOC"),
    "x-office-spreadsheet": ("#78E6A0", "grid", "XLS"),
    "x-office-presentation": ("#FFBE5A", "chart", "PPT"),
    "application-msword": ("#5FB4F0", "lines", "DOC"),
    "application-rtf": ("#5FB4F0", "lines", "RTF"),
    "application-vnd.ms-excel": ("#78E6A0", "grid", "XLS"),
    "application-vnd.ms-powerpoint": ("#FFBE5A", "chart", "PPT"),
    "application-vnd.oasis.opendocument.text": ("#5FB4F0", "lines", "ODT"),
    "application-vnd.oasis.opendocument.spreadsheet": ("#78E6A0", "grid", "ODS"),
    "application-vnd.oasis.opendocument.presentation": ("#FFBE5A", "chart", "ODP"),
    "application-vnd.oasis.opendocument.graphics": ("#FF8CBE", "image", "ODG"),
    "application-vnd.openxmlformats-officedocument.wordprocessingml.document": (
        "#5FB4F0", "lines", "DOCX"),
    "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet": (
        "#78E6A0", "grid", "XLSX"),
    "application-vnd.openxmlformats-officedocument.presentationml.presentation": (
        "#FFBE5A", "chart", "PPTX"),
    "font-x-generic": ("#C8AAB4", "font", "Aa"),
    "font-ttf": ("#C8AAB4", "font", "TTF"),
    "font-otf": ("#C8AAB4", "font", "OTF"),
    "application-x-iso9660-image": ("#C8AAB4", "disc", "ISO"),
    "application-x-cd-image": ("#C8AAB4", "disc", "ISO"),
    "application-x-deb": ("#E23A44", "package", "DEB"),
    "application-x-rpm": ("#E23A44", "package", "RPM"),
    "application-x-msi": ("#5FB4F0", "package", "MSI"),
    "application-vnd.android.package-archive": ("#78E6A0", "package", "APK"),
    "package-x-generic": ("#FFBE5A", "package", None),
    "text-markdown": ("#7FF0F0", "lines", "MD"),
    "text-x-markdown": ("#7FF0F0", "lines", "MD"),
    "application-x-php": ("#8A9BE8", "code", "PHP"),
    "application-x-ruby": ("#E23A44", "code", "RB"),
    "application-x-lua": ("#5FB4F0", "code", "LUA"),
    "text-x-csharp": ("#78E6A0", "code", "C#"),
    "application-x-sqlite3": ("#5FB4F0", "grid", "DB"),
    "application-x-bittorrent": ("#78E6A0", "download", "TOR"),
    "application-epub+zip": ("#FFBE5A", "lines", "EPUB"),
    "image-gif": ("#FF8CBE", "image", "GIF"),
    "image-webp": ("#FF8CBE", "image", "WEBP"),
    "image-bmp": ("#FF8CBE", "image", "BMP"),
    "image-tiff": ("#FF8CBE", "image", "TIFF"),
    "audio-flac": ("#78E6A0", "note", "FLAC"),
    "audio-x-wav": ("#78E6A0", "note", "WAV"),
    "audio-ogg": ("#78E6A0", "note", "OGG"),
    "video-x-matroska": ("#FFBE5A", "play", "MKV"),
    "video-webm": ("#FFBE5A", "play", "WEBM"),
    "application-x-appimage": ("#78E6A0", "package", "APP"),
    "application-vnd.flatpak": ("#5FB4F0", "package", "FLAT"),
}

# Archives use the normal folder silhouette with a zipper, so compressed
# folders are immediately recognisable as folders instead of generic files.
ARCHIVES = {
    "application-zip": "#781C2C",
    "application-x-compressed-tar": "#FFBE5A",
    "application-x-tar": "#FFBE5A",
    "application-x-7z-compressed": "#FF8CBE",
    "application-x-rar": "#FF8CBE",
    "application-x-bzip-compressed-tar": "#FFBE5A",
    "application-x-xz-compressed-tar": "#FFBE5A",
    "application-x-zstd-compressed-tar": "#FFBE5A",
    "application-gzip": "#FFBE5A",
    "application-x-gzip": "#FFBE5A",
    "application-vnd.rar": "#FF8CBE",
    "application-x-zip": "#781C2C",
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

# Smaller, shifted paw so it does not clash with the large folder sticker.
SMALL_PAW = f'<g transform="translate(13 5) scale(0.7)">{PAW}</g>'


def lighten(hex_color: str, amount: float = 0.22) -> str:
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    channels = [round(c + (255 - c) * amount) for c in (r, g, b)]
    return "#" + "".join(f"{c:02X}" for c in channels)


def glyph(kind: str, color: str, badge: bool = False) -> str:
    """Return a small glyph centred on (0,0), roughly -10..10 units."""
    ink = INK
    paper = PAPER
    parts = []
    if badge:
        parts.append(
            f'<rect x="-11" y="-11" width="22" height="22" rx="5" '
            f'fill="{paper}" stroke="{ink}" stroke-width="1.5"/>'
        )

    if kind == "lines":
        parts.append(
            f'<path d="M-8 -5 H8 M-8 0 H8 M-8 5 H4" fill="none" '
            f'stroke="{ink}" stroke-width="2" stroke-linecap="round"/>'
        )
    elif kind == "doc":
        parts.append(
            f'<path d="M-7 -9 H2 L7 -4 V9 H-7 Z" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M2 -9 V-4 H7" fill="none" stroke="{ink}" '
            f'stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M-4 -0.5 H4 M-4 2.5 H4 M-4 5.5 H1" stroke="{ink}" '
            f'stroke-width="1.3" stroke-linecap="round"/>'
        )
    elif kind == "film":
        parts.append(
            f'<rect x="-9" y="-7" width="18" height="14" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<rect x="-7" y="-5.5" width="2" height="2" fill="{paper}"/>'
            f'<rect x="-2" y="-5.5" width="2" height="2" fill="{paper}"/>'
            f'<rect x="3" y="-5.5" width="2" height="2" fill="{paper}"/>'
            f'<rect x="-7" y="3.5" width="2" height="2" fill="{paper}"/>'
            f'<rect x="-2" y="3.5" width="2" height="2" fill="{paper}"/>'
            f'<rect x="3" y="3.5" width="2" height="2" fill="{paper}"/>'
            f'<path d="M-2 -3 L4 0 L-2 3 Z" fill="{paper}" stroke="{ink}" '
            f'stroke-width="1.1" stroke-linejoin="round"/>'
        )
    elif kind == "code":
        parts.append(
            f'<text x="0" y="4" text-anchor="middle" font-family="monospace" '
            f'font-size="13" font-weight="700" fill="{ink}">&lt;/&gt;</text>'
        )
    elif kind == "braces":
        parts.append(
            f'<text x="0" y="5" text-anchor="middle" font-family="monospace" '
            f'font-size="15" font-weight="700" fill="{ink}">{{ }}</text>'
        )
    elif kind == "hash":
        parts.append(
            f'<text x="0" y="5" text-anchor="middle" font-family="monospace" '
            f'font-size="16" font-weight="700" fill="{ink}">#</text>'
        )
    elif kind == "note":
        parts.append(
            f'<path d="M2 -8 V6" stroke="{ink}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<ellipse cx="-2" cy="7" rx="4" ry="3" fill="{color}" stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M2 -8 C7 -8 8 -5 9 -2" fill="none" stroke="{ink}" '
            f'stroke-width="2" stroke-linecap="round"/>'
        )
    elif kind == "play":
        parts.append(
            f'<rect x="-9" y="-7" width="18" height="14" rx="3" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M-3 -4 L5 0 L-3 4 Z" fill="{paper}" stroke="{ink}" '
            f'stroke-width="1.2" stroke-linejoin="round"/>'
        )
    elif kind == "image":
        parts.append(
            f'<rect x="-9" y="-7" width="18" height="14" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<circle cx="-4" cy="-3" r="2" fill="{paper}" stroke="{ink}" stroke-width="1"/>'
            f'<path d="M-8 5 L-2 -1 L2 3 L5 0 L9 5 Z" fill="{paper}" '
            f'stroke="{ink}" stroke-width="1.2" stroke-linejoin="round"/>'
        )
    elif kind == "zip":
        parts.append(
            f'<rect x="-5" y="-9" width="10" height="18" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M0 -8 V6" stroke="{ink}" stroke-width="1.2" '
            f'stroke-dasharray="1.5 1.5"/>'
            f'<path d="M-3 6 H3 L2 9 H-2 Z" fill="{paper}" stroke="{ink}" stroke-width="1"/>'
        )
    elif kind == "grid":
        parts.append(
            f'<rect x="-9" y="-7" width="18" height="14" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M-3 -7 V7 M3 -7 V7 M-9 0 H9" stroke="{ink}" stroke-width="1"/>'
        )
    elif kind == "grid4":
        parts.append(
            f'<rect x="-8" y="-8" width="7" height="7" rx="1.5" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.2"/>'
            f'<rect x="1" y="-8" width="7" height="7" rx="1.5" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.2"/>'
            f'<rect x="-8" y="1" width="7" height="7" rx="1.5" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.2"/>'
            f'<rect x="1" y="1" width="7" height="7" rx="1.5" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.2"/>'
        )
    elif kind == "chart":
        parts.append(
            f'<rect x="-9" y="-7" width="18" height="14" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<rect x="-6" y="0" width="3" height="5" fill="{paper}"/>'
            f'<rect x="-1" y="-3" width="3" height="8" fill="{paper}"/>'
            f'<rect x="4" y="2" width="3" height="3" fill="{paper}"/>'
        )
    elif kind == "exec":
        parts.append(
            f'<rect x="-9" y="-7" width="18" height="14" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<text x="-6" y="3" font-family="monospace" font-size="8" '
            f'font-weight="700" fill="{paper}">&gt;_</text>'
        )
    elif kind == "shell":
        parts.append(
            f'<text x="0" y="6" text-anchor="middle" font-family="monospace" '
            f'font-size="17" font-weight="700" fill="{ink}">$</text>'
        )
    elif kind == "font":
        parts.append(
            f'<text x="0" y="7" text-anchor="middle" font-family="serif" '
            f'font-size="20" font-weight="700" fill="{color}" '
            f'stroke="{ink}" stroke-width="1">A</text>'
        )
    elif kind == "disc":
        parts.append(
            f'<circle cx="0" cy="0" r="9" fill="{color}" stroke="{ink}" stroke-width="1.5"/>'
            f'<circle cx="0" cy="0" r="2.5" fill="{paper}" stroke="{ink}" stroke-width="1"/>'
        )
    elif kind == "package":
        parts.append(
            f'<path d="M-9 -7 H9 V7 H-9 Z" fill="{color}" stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M-9 -2 H9" stroke="{ink}" stroke-width="1"/>'
            f'<path d="M0 -7 V7" stroke="{paper}" stroke-width="2"/>'
        )
    elif kind == "download":
        parts.append(
            f'<path d="M0 -8 V5 M-5 0 L0 6 L5 0" fill="none" stroke="{ink}" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M-8 8 H8" stroke="{ink}" stroke-width="2" stroke-linecap="round"/>'
        )
    elif kind == "globe":
        parts.append(
            f'<circle cx="0" cy="0" r="9" fill="{color}" stroke="{ink}" stroke-width="1.5"/>'
            f'<ellipse cx="0" cy="0" rx="4" ry="9" fill="none" stroke="{ink}" stroke-width="1"/>'
            f'<path d="M-9 0 H9" stroke="{ink}" stroke-width="1"/>'
        )
    elif kind == "gear":
        parts.append(
            f'<circle cx="0" cy="0" r="4" fill="{paper}" stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M0 -9 V-5 M0 5 V9 M-9 0 H-5 M5 0 H9 '
            f'M-6 -6 L-3 -3 M3 3 L6 6 M6 -6 L3 -3 M-3 3 L-6 6" '
            f'stroke="{ink}" stroke-width="2" stroke-linecap="round"/>'
        )
    elif kind == "gamepad":
        parts.append(
            f'<rect x="-9" y="-5" width="18" height="10" rx="5" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M-4 0 H0 M-2 -2 V2" stroke="{paper}" stroke-width="1.5"/>'
            f'<circle cx="4" cy="-1" r="1.2" fill="{paper}"/>'
            f'<circle cx="6" cy="2" r="1.2" fill="{paper}"/>'
        )
    elif kind == "plus":
        parts.append(
            f'<path d="M0 -8 V8 M-8 0 H8" stroke="{ink}" stroke-width="3" '
            f'stroke-linecap="round"/>'
        )
    elif kind == "share":
        parts.append(
            f'<circle cx="-6" cy="0" r="3" fill="{color}" stroke="{ink}" stroke-width="1.2"/>'
            f'<circle cx="6" cy="-6" r="3" fill="{color}" stroke="{ink}" stroke-width="1.2"/>'
            f'<circle cx="6" cy="6" r="3" fill="{color}" stroke="{ink}" stroke-width="1.2"/>'
            f'<path d="M-3 -1 L3 -5 M-3 1 L3 5" stroke="{ink}" stroke-width="1.2"/>'
        )
    elif kind == "star":
        parts.append(
            f'<path d="M0 -9 L2.6 -3 L9 -2.4 L4.4 1.8 L5.6 8.2 L0 5 L-5.6 8.2 '
            f'L-4.4 1.8 L-9 -2.4 L-2.6 -3 Z" fill="{color}" stroke="{ink}" '
            f'stroke-width="1.2" stroke-linejoin="round"/>'
        )
    elif kind == "monitor":
        parts.append(
            f'<rect x="-9" y="-7" width="18" height="12" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M-3 5 V8 M3 5 V8 M-6 8 H6" stroke="{ink}" stroke-width="2" '
            f'stroke-linecap="round"/>'
        )
    elif kind == "home":
        parts.append(
            f'<path d="M-9 0 L0 -8 L9 0" fill="none" stroke="{ink}" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M-6 -1 V8 H6 V-1" fill="none" stroke="{ink}" stroke-width="2.5" '
            f'stroke-linejoin="round"/>'
        )
    elif kind == "printer":
        parts.append(
            f'<rect x="-7" y="-2" width="14" height="8" rx="2" fill="{color}" '
            f'stroke="{ink}" stroke-width="1.5"/>'
            f'<rect x="-5" y="-8" width="10" height="6" fill="{paper}" '
            f'stroke="{ink}" stroke-width="1.2"/>'
            f'<rect x="-4" y="5" width="8" height="4" fill="{paper}" '
            f'stroke="{ink}" stroke-width="1"/>'
        )
    elif kind == "clock":
        parts.append(
            f'<circle cx="0" cy="0" r="9" fill="{color}" stroke="{ink}" stroke-width="1.5"/>'
            f'<path d="M0 -5 V0 L4 3" fill="none" stroke="{ink}" stroke-width="2" '
            f'stroke-linecap="round"/>'
        )
    elif kind == "readme":
        parts.append(
            f'<path d="M-8 -6 H8 M-8 -1 H8 M-8 4 H4" fill="none" stroke="{ink}" '
            f'stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="7" cy="6" r="2.5" fill="{color}" stroke="{ink}" stroke-width="1"/>'
        )
    elif kind == "changelog":
        parts.append(
            f'<path d="M-8 -6 H8 M-8 0 H8 M-8 6 H6" fill="none" stroke="{ink}" '
            f'stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="-9" cy="-6" r="1.3" fill="{color}"/>'
            f'<circle cx="-9" cy="0" r="1.3" fill="{color}"/>'
            f'<circle cx="-9" cy="6" r="1.3" fill="{color}"/>'
        )
    return "".join(parts)


def folder_svg(
    color: str,
    open_folder: bool = False,
    symbol: str | None = None,
    archive: bool = False,
) -> str:
    if open_folder:
        color = lighten(color)
    extra = ""
    paw = PAW
    if archive:
        extra = f"""
  <rect x="21.5" y="22" width="5" height="19" rx="1.5" fill="{PAPER}" opacity="0.92"/>
  <path d="M24 22.5 V40.5" stroke="{INK}" stroke-width="1.2" stroke-dasharray="1.5 1.3"/>
  <rect x="21" y="29" width="6" height="3.6" rx="1" fill="{color}" stroke="{INK}" stroke-width="1.1"/>
  <path d="M24 32.6 V35.4" stroke="{INK}" stroke-width="1.2" stroke-linecap="round"/>
  <rect x="22.4" y="35.4" width="3.2" height="2.2" rx="0.8" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>
"""
    elif symbol:
        # A large paper sticker with a coloured top tab: readable even at
        # 32 px, unlike the small badge used by the original icons.
        extra = f"""
  <g transform="translate(19 31)">
    <rect x="-12" y="-9" width="26" height="22" rx="6" fill="{INK}" opacity="0.35"/>
    <rect x="-13" y="-11" width="26" height="22" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>
    <g transform="translate(0 1) scale(0.9)">{glyph(symbol, color)}</g>
  </g>
"""
        paw = SMALL_PAW
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <path d="{BACK}" transform="translate(3 3)" fill="{INK}" opacity="0.9"/>
  <path d="{BACK}" fill="{PLUM}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="{FRONT}" fill="{color}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="{HIGHLIGHT}" fill="{PAPER}" opacity="0.30"/>
{extra}
{paw}</svg>
"""


def file_svg(color: str, symbol: str = "lines", label: str | None = None) -> str:
    label_svg = ""
    if label:
        label_svg = (
            f'<text x="19" y="11" text-anchor="middle" font-family="Nunito, sans-serif" '
            f'font-size="5.4" font-weight="800" fill="{PAPER}">{label}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <path d="M9 3 H29 L39 13 V43 A2 2 0 0 1 37 45 H9 A2 2 0 0 1 7 43 V5 A2 2 0 0 1 9 3 Z"
        transform="translate(3 3)" fill="{INK}" opacity="0.9"/>
  <path d="M9 3 H29 L39 13 V43 A2 2 0 0 1 37 45 H9 A2 2 0 0 1 7 43 V5 A2 2 0 0 1 9 3 Z"
        fill="{PAPER}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M29 3 V13 H39" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>
  <rect x="11" y="6" width="15" height="6" rx="2" fill="{color}" stroke="{INK}" stroke-width="1.5"/>
{label_svg}
  <g transform="translate(24 29)">{glyph(symbol, color)}</g>
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


for name, (color, symbol) in FOLDERS.items():
    is_archive = name == "folder-archives"
    (PLACES / f"{name}.svg").write_text(
        folder_svg(
            color,
            symbol=None if is_archive else symbol,
            archive=is_archive,
        ),
        encoding="utf-8",
    )
    (PLACES / f"{name}-open.svg").write_text(
        folder_svg(
            color,
            open_folder=True,
            symbol=None if is_archive else symbol,
            archive=is_archive,
        ),
        encoding="utf-8",
    )

for name, (color, symbol, label) in FILES.items():
    (MIMETYPES / f"{name}.svg").write_text(
        file_svg(color, symbol=symbol, label=label), encoding="utf-8"
    )

for name, color in ARCHIVES.items():
    (MIMETYPES / f"{name}.svg").write_text(
        folder_svg(color, archive=True), encoding="utf-8"
    )

(PLACES / "user-trash.svg").write_text(trash_svg(), encoding="utf-8")
(PLACES / "user-trash-full.svg").write_text(trash_svg(), encoding="utf-8")

print(
    f"Generated {len(FOLDERS) * 2 + len(FILES) + len(ARCHIVES) + 2} icons "
    f"({PLACES}, {MIMETYPES})"
)
