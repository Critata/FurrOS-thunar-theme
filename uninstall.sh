#!/usr/bin/env bash
# Rimuove il tema FurrOS e ripristina Papirus-Dark / Adwaita.
set -euo pipefail

HOME_DIR="${HOME:-/home/$(id -un)}"
STAMP="$(date +%Y%m%d-%H%M%S)"

echo "FurrOS Thunar theme — disinstallazione"

python3 - "$HOME_DIR" "$STAMP" <<'PY'
import sys
from pathlib import Path

home, stamp = Path(sys.argv[1]), sys.argv[2]
values = {
    "gtk-theme-name": "Adwaita",
    "gtk-icon-theme-name": "Papirus-Dark",
    "gtk-application-prefer-dark-theme": "1",
}
for rel in (".config/gtk-3.0/settings.ini", ".config/gtk-4.0/settings.ini"):
    path = home / rel
    if not path.exists():
        continue
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line and not line.startswith("[") else None
        out.append(f"{key}={values[key]}" if key in values else line)
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
PY

if command -v gsettings >/dev/null 2>&1; then
  gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita' || true
  gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark' || true
  gsettings set org.gnome.desktop.interface color-scheme 'default' || true
fi

USER_CSS="$HOME_DIR/.config/gtk-3.0/gtk.css"
if [[ -f "$USER_CSS" ]]; then
  LAST_BACKUP=$(ls -1 "$USER_CSS".bak-* 2>/dev/null | sort | tail -n 1 || true)
  if [[ -n "$LAST_BACKUP" ]]; then
    cp -a "$LAST_BACKUP" "$USER_CSS"
    echo "  ripristinato: $USER_CSS <- $LAST_BACKUP"
  else
    rm -f "$USER_CSS"
    echo "  rimosso: $USER_CSS"
  fi
fi

rm -rf "$HOME_DIR/.themes/FurrOS" "$HOME_DIR/.local/share/icons/FurrOS-Papirus"

if [[ -f "$(dirname "${BASH_SOURCE[0]}")/libreoffice/uninstall.sh" ]]; then
  if pgrep -x soffice.bin >/dev/null 2>&1; then
    echo "  LibreOffice è aperto: chiudi i documenti e lancia libreoffice/uninstall.sh"
  else
    bash "$(dirname "${BASH_SOURCE[0]}")/libreoffice/uninstall.sh"
  fi
fi

if pgrep -x thunar >/dev/null 2>&1; then
  pkill -TERM thunar || true
  sleep 1
fi
if command -v thunar >/dev/null 2>&1; then
  setsid thunar --daemon >/dev/null 2>&1 &
fi

echo "Disinstallazione completata."
