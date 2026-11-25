#!/usr/bin/env bash
# Installa il tema FurrOS per Thunar (GTK3) nella home dell'utente corrente.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${HOME:-/home/$(id -un)}"
STAMP="$(date +%Y%m%d-%H%M%S)"

echo "FurrOS Thunar theme — installazione"
echo "  Sorgente : $ROOT"
echo "  Destinazione : $HOME_DIR"

# ---------------------------------------------------------------------------
# Tema GTK3
# ---------------------------------------------------------------------------
mkdir -p "$HOME_DIR/.themes/FurrOS/gtk-3.0/assets"
cp -a "$ROOT/gtk3/gtk-3.0/gtk.css" "$HOME_DIR/.themes/FurrOS/gtk-3.0/gtk.css"
cp -a "$ROOT/gtk3/gtk-3.0/assets/furros-watermark.png" \
  "$HOME_DIR/.themes/FurrOS/gtk-3.0/assets/furros-watermark.png"
cp -a "$ROOT/gtk3/index.theme" "$HOME_DIR/.themes/FurrOS/index.theme"

# ---------------------------------------------------------------------------
# Icone
# ---------------------------------------------------------------------------
mkdir -p "$HOME_DIR/.local/share/icons/FurrOS-Papirus"
cp -a "$ROOT/icons/FurrOS-Papirus/." "$HOME_DIR/.local/share/icons/FurrOS-Papirus/"

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f -q "$HOME_DIR/.local/share/icons/FurrOS-Papirus" || true
fi

# ---------------------------------------------------------------------------
# settings.ini: aggiorna le chiavi mantenendo tutte le altre impostazioni
# ---------------------------------------------------------------------------
python3 - "$HOME_DIR" "$STAMP" <<'PY'
import sys
from pathlib import Path

home, stamp = Path(sys.argv[1]), sys.argv[2]
values = {
    "gtk-theme-name": "FurrOS",
    "gtk-icon-theme-name": "FurrOS-Papirus",
    "gtk-font-name": "Nunito 11",
    "gtk-application-prefer-dark-theme": "1",
}

for rel in (".config/gtk-3.0/settings.ini", ".config/gtk-4.0/settings.ini"):
    path = home / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(path.name + f".bak-{stamp}")
        backup.write_bytes(path.read_bytes())
        print(f"  backup: {backup}")
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        lines = ["[Settings]"]

    if not any(line.strip() == "[Settings]" for line in lines):
        lines = ["[Settings]"] + lines

    out, seen = [], set()
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line and not line.startswith("[") else None
        if key in values:
            out.append(f"{key}={values[key]}")
            seen.add(key)
        else:
            out.append(line)

    for key, value in values.items():
        if key not in seen:
            out.append(f"{key}={value}")

    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"  aggiornato: {path}")
PY

# ---------------------------------------------------------------------------
# GSettings / restart di Thunar
# ---------------------------------------------------------------------------
if command -v gsettings >/dev/null 2>&1; then
  gsettings set org.gnome.desktop.interface gtk-theme 'FurrOS' || true
  gsettings set org.gnome.desktop.interface icon-theme 'FurrOS-Papirus' || true
  gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark' || true
fi

if pgrep -x thunar >/dev/null 2>&1; then
  pkill -TERM thunar || true
  sleep 1
fi
if command -v thunar >/dev/null 2>&1; then
  setsid thunar --daemon >/dev/null 2>&1 &
fi

echo "Installazione completata. Se Thunar era aperto, è stato riavviato."
echo "Verifica:"
echo "  gsettings get org.gnome.desktop.interface gtk-theme"
echo "  gsettings get org.gnome.desktop.interface icon-theme"
