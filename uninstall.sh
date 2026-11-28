#!/usr/bin/env bash
# Rimuove il tema FurrOS e ripristina il tema GTK/icone precedenti.
set -euo pipefail

HOME_DIR="${HOME:-/home/$(id -un)}"
STAMP="$(date +%Y%m%d-%H%M%S)"
CONFIG_DIR="$HOME_DIR/.config/furros"
PREV_FILE="$CONFIG_DIR/previous-settings"

echo "FurrOS Thunar theme — disinstallazione"

previous_value() {
  sed -n "s/^$1=//p" "$PREV_FILE" 2>/dev/null | head -n1 || true
}

GTK_THEME="$(previous_value gtk-theme)"
ICON_THEME="$(previous_value icon-theme)"
COLOR_SCHEME="$(previous_value color-scheme)"
FONT_NAME="$(previous_value font-name)"
PREFER_DARK="$(previous_value prefer-dark)"
case "$GTK_THEME" in
  ""|FurrOS|FurrOS-*)
    if [ -f "$HOME_DIR/.themes/adw-gtk3-dark/gtk-3.0/gtk.css" ] \
      || [ -f "$HOME_DIR/.local/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css" ] \
      || [ -f "/usr/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css" ]; then
      GTK_THEME="adw-gtk3-dark"
    else
      GTK_THEME="Adwaita"
    fi
    ;;
esac
case "$ICON_THEME" in
  ""|FurrOS|FurrOS-*)
    if [ -d "$HOME_DIR/.local/share/icons/Papirus-Dark" ] \
      || [ -d "$HOME_DIR/.icons/Papirus-Dark" ] \
      || [ -d "/usr/share/icons/Papirus-Dark" ]; then
      ICON_THEME="Papirus-Dark"
    else
      ICON_THEME="Adwaita"
    fi
    ;;
esac
[ -n "$COLOR_SCHEME" ] || COLOR_SCHEME="default"

python3 - "$HOME_DIR" "$GTK_THEME" "$ICON_THEME" "$FONT_NAME" "$PREFER_DARK" <<'PY'
import sys
from pathlib import Path

home = Path(sys.argv[1])
theme, icons, font, prefer_dark = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
values = {
    "gtk-theme-name": theme,
    "gtk-icon-theme-name": icons,
}
remove = set()
if font:
    values["gtk-font-name"] = font
else:
    remove.add("gtk-font-name")
if prefer_dark:
    values["gtk-application-prefer-dark-theme"] = prefer_dark
else:
    remove.add("gtk-application-prefer-dark-theme")

for rel in (".config/gtk-3.0/settings.ini", ".config/gtk-4.0/settings.ini"):
    path = home / rel
    if not path.exists():
        continue
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line and not line.startswith("[") else None
        if key in remove:
            continue
        out.append(f"{key}={values[key]}" if key in values else line)
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
PY

if command -v gsettings >/dev/null 2>&1; then
  gsettings set org.gnome.desktop.interface gtk-theme "$GTK_THEME" || true
  gsettings set org.gnome.desktop.interface icon-theme "$ICON_THEME" || true
  gsettings set org.gnome.desktop.interface color-scheme "$COLOR_SCHEME" || true
  if [ -n "$FONT_NAME" ]; then
    gsettings set org.gnome.desktop.interface font-name "$FONT_NAME" || true
  fi
fi

rm -rf \
  "$HOME_DIR/.themes/FurrOS" \
  "$HOME_DIR/.local/share/themes/FurrOS" \
  "$HOME_DIR/.local/share/icons/FurrOS-Papirus" \
  "$HOME_DIR/.icons/FurrOS-Papirus"

# Ripristina il CSS GTK4 dell'utente (o lo rimuove se non c'era).
GTK4_USER="$HOME_DIR/.config/gtk-4.0/gtk.css"
if [ -f "$GTK4_USER" ] && grep -q 'FurrOS GTK4' "$GTK4_USER"; then
  LATEST_GTK4="$(ls -1t "$GTK4_USER".bak-* 2>/dev/null | head -n1 || true)"
  if [ -n "$LATEST_GTK4" ]; then
    cp -a "$LATEST_GTK4" "$GTK4_USER"
  else
    rm -f "$GTK4_USER"
  fi
fi

# Ripristina il vecchio override GTK3 per LibreOffice, se era presente.
OLD_OVERRIDE="$HOME_DIR/.config/gtk-3.0/gtk.css"
if [ -f "$OLD_OVERRIDE" ] && grep -q 'FurrOS high-priority GTK3 override' "$OLD_OVERRIDE"; then
  LATEST_OVERRIDE="$(ls -1t "$OLD_OVERRIDE".bak-* 2>/dev/null | head -n1 || true)"
  if [ -n "$LATEST_OVERRIDE" ]; then
    cp -a "$LATEST_OVERRIDE" "$OLD_OVERRIDE"
  else
    rm -f "$OLD_OVERRIDE"
  fi
fi

# Rimuove il wrapper LibreOffice e i suoi alias.
for alias in furros-libreoffice soffice libreoffice lowriter localc loimpress lodraw lobase lomath; do
  path="$HOME_DIR/.local/bin/$alias"
  if [ -L "$path" ] && [ "$(readlink "$path")" = "furros-libreoffice" ]; then
    rm -f "$path"
  fi
done
rm -f "$HOME_DIR/.local/bin/furros-libreoffice"

# Rimuove gli override .desktop creati da install.sh.
python3 - "$HOME_DIR" <<'PY'
import sys
from pathlib import Path

apps = Path(sys.argv[1]) / ".local/share/applications"
if apps.is_dir():
    for path in apps.glob("libreoffice-*.desktop"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if "X-FurrOS-LibreOffice=true" in text:
            path.unlink()
            print(f"  rimosso: {path}")
PY
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$HOME_DIR/.local/share/applications" >/dev/null 2>&1 || true
fi

# Rimuove l'eventuale palette FurrOS dal registro di LibreOffice.
python3 - "$HOME_DIR" "$STAMP" <<'PY'
import re
import shutil
import sys
from pathlib import Path

home = Path(sys.argv[1])
stamp = sys.argv[2]
for reg in sorted(home.glob(".config/libreoffice/*/user/registrymodifications.xcu")):
    try:
        text = reg.read_text(encoding="utf-8")
    except OSError:
        continue
    if "<!-- FurrOS LibreOffice palette -->" not in text:
        continue
    shutil.copy2(reg, reg.with_name(reg.name + f".bak-{stamp}"))
    text = re.sub(
        r"\s*<!-- FurrOS LibreOffice palette -->.*?<!-- /FurrOS LibreOffice palette -->\s*",
        "\n",
        text,
        flags=re.S,
    )
    reg.write_text(text, encoding="utf-8")
    print(f"  palette FurrOS rimossa da {reg}")
PY

rm -rf "$CONFIG_DIR"

if pgrep -x thunar >/dev/null 2>&1; then
  pkill -TERM thunar || true
  sleep 1
fi
if command -v thunar >/dev/null 2>&1; then
  setsid thunar --daemon >/dev/null 2>&1 &
fi

echo "Disinstallazione completata."
