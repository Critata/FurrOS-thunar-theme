#!/usr/bin/env bash
# Installa il tema FurrOS per Thunar (GTK3/GTK4) nella home dell'utente corrente.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${HOME:-/home/$(id -un)}"
STAMP="$(date +%Y%m%d-%H%M%S)"
CONFIG_DIR="$HOME_DIR/.config/furros"
PREV_FILE="$CONFIG_DIR/previous-settings"
LO_THEME_FILE="$CONFIG_DIR/libreoffice-theme"

echo "FurrOS Thunar theme — installazione"
echo "  Sorgente : $ROOT"
echo "  Destinazione : $HOME_DIR"

# ---------------------------------------------------------------------------
# Salva le impostazioni correnti, così LibreOffice e la disinstallazione
# possono tornare al tema precedente invece di forzare sempre Adwaita.
# ---------------------------------------------------------------------------
PREV_GTK=""
PREV_ICON=""
PREV_COLOR=""
PREV_FONT=""
PREV_DARK=""
if command -v gsettings >/dev/null 2>&1; then
  PREV_GTK="$(gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null | tr -d "'" || true)"
  PREV_ICON="$(gsettings get org.gnome.desktop.interface icon-theme 2>/dev/null | tr -d "'" || true)"
  PREV_COLOR="$(gsettings get org.gnome.desktop.interface color-scheme 2>/dev/null | tr -d "'" || true)"
  PREV_FONT="$(gsettings get org.gnome.desktop.interface font-name 2>/dev/null | tr -d "'" || true)"
fi

# GTK's settings.ini is what GTK3 apps actually read, so prefer it when it
# already exists (for example after a previous FurrOS install).
ini_value() {
  sed -n "s/^$1=//p" "$HOME_DIR/.config/gtk-3.0/settings.ini" 2>/dev/null | head -n1 || true
}
GTK_INI="$(ini_value gtk-theme-name)"
ICON_INI="$(ini_value gtk-icon-theme-name)"
FONT_INI="$(ini_value gtk-font-name)"
DARK_INI="$(ini_value gtk-application-prefer-dark-theme)"
[ -n "$GTK_INI" ] && PREV_GTK="$GTK_INI"
[ -n "$ICON_INI" ] && PREV_ICON="$ICON_INI"
[ -n "$FONT_INI" ] && PREV_FONT="$FONT_INI"
[ -n "$DARK_INI" ] && PREV_DARK="$DARK_INI"
case "$PREV_GTK" in
  ""|FurrOS|FurrOS-*)
    if [ -f "$HOME_DIR/.themes/adw-gtk3-dark/gtk-3.0/gtk.css" ] \
      || [ -f "$HOME_DIR/.local/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css" ] \
      || [ -f "/usr/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css" ]; then
      PREV_GTK="adw-gtk3-dark"
    else
      PREV_GTK="Adwaita"
    fi
    ;;
esac
case "$PREV_ICON" in
  ""|FurrOS|FurrOS-*)
    if [ -d "$HOME_DIR/.local/share/icons/Papirus-Dark" ] \
      || [ -d "$HOME_DIR/.icons/Papirus-Dark" ] \
      || [ -d "/usr/share/icons/Papirus-Dark" ]; then
      PREV_ICON="Papirus-Dark"
    else
      PREV_ICON="Adwaita"
    fi
    ;;
esac
[ -n "$PREV_COLOR" ] || PREV_COLOR="default"

mkdir -p "$CONFIG_DIR"
{
  printf 'gtk-theme=%s\n' "$PREV_GTK"
  printf 'icon-theme=%s\n' "$PREV_ICON"
  printf 'color-scheme=%s\n' "$PREV_COLOR"
  printf 'font-name=%s\n' "$PREV_FONT"
  printf 'prefer-dark=%s\n' "$PREV_DARK"
} > "$PREV_FILE"
printf '%s\n' "$PREV_GTK" > "$LO_THEME_FILE"

# ---------------------------------------------------------------------------
# Scegli la base GTK3 disponibile. Su distribuzioni senza adw-gtk3-dark
# (per esempio Zorin OS) si usa il tema di sistema (Zorin/Adwaita/...), così
# le regole FurrOS restano applicate invece di essere ignorate.
# ---------------------------------------------------------------------------
BASE_THEME=""
for candidate in \
  "$HOME_DIR/.themes/adw-gtk3-dark/gtk-3.0/gtk.css" \
  "$HOME_DIR/.local/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css" \
  "/usr/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css" \
  "/usr/local/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css" \
  "/usr/share/themes/Adwaita/gtk-3.0/gtk.css" \
  "/usr/share/themes/Adwaita-dark/gtk-3.0/gtk.css" \
  /usr/share/themes/Zorin*/gtk-3.0/gtk.css \
  /usr/share/themes/Greybird*/gtk-3.0/gtk.css \
  /usr/share/themes/Arc*/gtk-3.0/gtk.css \
  /usr/share/themes/Materia*/gtk-3.0/gtk.css \
  /usr/share/themes/Numix*/gtk-3.0/gtk.css; do
  if [ -f "$candidate" ]; then
    BASE_THEME="$candidate"
    break
  fi
done

# Last resort: any complete GTK3 theme shipped by the distribution.
if [ -z "$BASE_THEME" ]; then
  BASE_THEME="$(find /usr/share/themes -maxdepth 3 -path '*/gtk-3.0/gtk.css' -print -quit 2>/dev/null || true)"
fi

if [ -n "$BASE_THEME" ]; then
  echo "  base GTK3: $BASE_THEME"
else
  echo "  ATTENZIONE: nessuna base GTK3 trovata."
  echo "  L'import verrà rimosso: restano attive solo le regole FurrOS."
fi

# ---------------------------------------------------------------------------
# Tema GTK3 + GTK4 in entrambe le directory usate dalle varie distro.
# ---------------------------------------------------------------------------
install_theme_dir() {
  local dir="$1"
  mkdir -p "$dir/gtk-3.0" "$dir/gtk-4.0"
  cp -a "$ROOT/gtk3/gtk-3.0/gtk.css" "$dir/gtk-3.0/gtk.css"
  cp -a "$ROOT/gtk3/index.theme" "$dir/index.theme"
  cp -a "$ROOT/gtk4/gtk-4.0/gtk.css" "$dir/gtk-4.0/gtk.css"
  python3 - "$dir/gtk-3.0/gtk.css" "$BASE_THEME" <<'PY'
import sys
from pathlib import Path

css = Path(sys.argv[1])
base = sys.argv[2]
text = css.read_text(encoding="utf-8")
needle = '@import url("/usr/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css");'
if base:
    if needle in text:
        text = text.replace(needle, f'@import url("{base}");', 1)
    else:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("@import"):
                lines[i] = f'@import url("{base}");'
                break
        text = "\n".join(lines) + "\n"
else:
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("@import")
    ) + "\n"
css.write_text(text, encoding="utf-8")
PY
}

install_theme_dir "$HOME_DIR/.themes/FurrOS"
install_theme_dir "$HOME_DIR/.local/share/themes/FurrOS"

# ---------------------------------------------------------------------------
# Icone: ~/.local/share/icons (freedesktop) e ~/.icons (legacy).
# ---------------------------------------------------------------------------
install_icon_dir() {
  local dir="$1"
  rm -rf "$dir"
  mkdir -p "$dir"
  cp -a "$ROOT/icons/FurrOS-Papirus/." "$dir/"
  find "$dir" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true
  if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -q "$dir" || true
  fi
}

install_icon_dir "$HOME_DIR/.local/share/icons/FurrOS-Papirus"
install_icon_dir "$HOME_DIR/.icons/FurrOS-Papirus"

# ---------------------------------------------------------------------------
# CSS GTK4 a priorità utente: copre Nautilus/GNOME Files e le app libadwaita
# che non leggono il tema GTK3.
# ---------------------------------------------------------------------------
GTK4_USER="$HOME_DIR/.config/gtk-4.0/gtk.css"
mkdir -p "$(dirname "$GTK4_USER")"
if [ -f "$GTK4_USER" ] && ! grep -q 'FurrOS GTK4' "$GTK4_USER"; then
  cp -a "$GTK4_USER" "$GTK4_USER.bak-$STAMP"
  echo "  backup: $GTK4_USER.bak-$STAMP"
fi
cp -a "$ROOT/gtk4/gtk-4.0/gtk.css" "$GTK4_USER"

# ---------------------------------------------------------------------------
# Rimuove il vecchio override GTK3 per LibreOffice, se presente.
# ---------------------------------------------------------------------------
OLD_OVERRIDE="$HOME_DIR/.config/gtk-3.0/gtk.css"
if [ -f "$OLD_OVERRIDE" ] && grep -q 'FurrOS high-priority GTK3 override' "$OLD_OVERRIDE"; then
  cp -a "$OLD_OVERRIDE" "$OLD_OVERRIDE.bak-$STAMP"
  rm -f "$OLD_OVERRIDE"
  echo "  rimosso vecchio override GTK per LibreOffice"
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
# LibreOffice: wrapper che forza il tema GTK precedente. Il tema FurrOS resta
# globale per Thunar, ma LibreOffice non lo eredita più.
# ---------------------------------------------------------------------------
SOFFICE_BIN=""
for candidate in \
  "/usr/lib/libreoffice/program/soffice" \
  "/usr/bin/soffice" \
  "/usr/local/bin/soffice" \
  "/snap/bin/soffice" \
  "/snap/bin/libreoffice"; do
  if [ -x "$candidate" ]; then
    SOFFICE_BIN="$candidate"
    break
  fi
done
if [ -z "$SOFFICE_BIN" ] && command -v soffice >/dev/null 2>&1; then
  SOFFICE_BIN="$(command -v soffice)"
fi

# LibreOffice may also be shipped as a Snap or Flatpak. In that case there is
# no native soffice binary, but the desktop files still need the wrapper.
LO_PRESENT=""
[ -n "$SOFFICE_BIN" ] && LO_PRESENT="1"
for dir in \
  "/usr/share/applications" \
  "/usr/local/share/applications" \
  "/var/lib/snapd/desktop/applications" \
  "/var/lib/flatpak/exports/share/applications" \
  "$HOME_DIR/.local/share/flatpak/exports/share/applications"; do
  if compgen -G "$dir/libreoffice-*.desktop" >/dev/null 2>&1; then
    LO_PRESENT="1"
    break
  fi
done

if [ -n "$LO_PRESENT" ]; then
  BIN_DIR="$HOME_DIR/.local/bin"
  WRAPPER="$BIN_DIR/furros-libreoffice"
  mkdir -p "$BIN_DIR"
  cat > "$WRAPPER" <<WRAPPER
#!/bin/sh
set -eu
theme_file="\${XDG_CONFIG_HOME:-\$HOME/.config}/furros/libreoffice-theme"
theme="Adwaita"
if [ -r "\$theme_file" ]; then
  IFS= read -r theme < "\$theme_file" || theme="Adwaita"
fi
case "\$theme" in
  ""|FurrOS|FurrOS-*) theme="Adwaita" ;;
esac
export GTK_THEME="\$theme"
export SAL_USE_VCLPLUGIN="\${SAL_USE_VCLPLUGIN:-gtk3}"
if [ "\${1:-}" = "--run" ]; then
  shift
  exec "\$@"
fi
case "\$(basename "\$0")" in
  lowriter) set -- --writer "\$@" ;;
  localc) set -- --calc "\$@" ;;
  loimpress) set -- --impress "\$@" ;;
  lodraw) set -- --draw "\$@" ;;
  lobase) set -- --base "\$@" ;;
  lomath) set -- --math "\$@" ;;
esac
if [ -z "$SOFFICE_BIN" ]; then
  echo "furros-libreoffice: soffice non trovato nel PATH" >&2
  exit 127
fi
exec "$SOFFICE_BIN" "\$@"
WRAPPER
  chmod +x "$WRAPPER"
  for alias in soffice libreoffice lowriter localc loimpress lodraw lobase lomath; do
    ln -sf "furros-libreoffice" "$BIN_DIR/$alias"
  done

  python3 - "$HOME_DIR" "$WRAPPER" <<'PY'
import re
import sys
from pathlib import Path

home = Path(sys.argv[1])
wrapper = sys.argv[2]
apps = {
    "libreoffice-writer.desktop": ("--writer %U", "LibreOffice Writer", "libreoffice-writer"),
    "libreoffice-calc.desktop": ("--calc %U", "LibreOffice Calc", "libreoffice-calc"),
    "libreoffice-impress.desktop": ("--impress %U", "LibreOffice Impress", "libreoffice-impress"),
    "libreoffice-draw.desktop": ("--draw %U", "LibreOffice Draw", "libreoffice-draw"),
    "libreoffice-base.desktop": ("--base %U", "LibreOffice Base", "libreoffice-base"),
    "libreoffice-math.desktop": ("--math %U", "LibreOffice Math", "libreoffice-math"),
    "libreoffice-startcenter.desktop": ("%U", "LibreOffice", "libreoffice-startcenter"),
}
src_dirs = [
    Path("/usr/share/applications"),
    Path("/usr/local/share/applications"),
    Path("/var/lib/snapd/desktop/applications"),
    Path("/var/lib/flatpak/exports/share/applications"),
    home / ".local/share/flatpak/exports/share/applications",
    home / ".local/share/applications",
]
dest = home / ".local/share/applications"
dest.mkdir(parents=True, exist_ok=True)

native = re.compile(
    r"^(?:libreoffice|soffice|/usr/bin/(?:libreoffice|soffice)"
    r"|/usr/lib/libreoffice/program/soffice)(?=\s|$)"
)

for name, (args, label, icon) in apps.items():
    src = next((d / name for d in src_dirs if (d / name).exists()), None)
    if src:
        text = src.read_text(encoding="utf-8")
    else:
        text = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            f"Name={label}\n"
            f"Icon={icon}\n"
            f"Exec=libreoffice {args}\n"
            "Terminal=false\n"
            "Categories=Office;\n"
        )
    out = []
    for line in text.splitlines():
        if line.startswith("Exec="):
            command = line[len("Exec="):].strip()
            if command.startswith(wrapper):
                pass
            elif native.match(command):
                command = wrapper + command[native.match(command).end():]
            else:
                command = f"{wrapper} --run {command}"
            line = f"Exec={command}"
        if line.startswith("X-FurrOS-LibreOffice="):
            continue
        out.append(line)
    out.append("X-FurrOS-LibreOffice=true")
    (dest / name).write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"  override: {dest / name}")
PY
  if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$HOME_DIR/.local/share/applications" >/dev/null 2>&1 || true
  fi
else
  echo "  LibreOffice non trovato: nessun wrapper creato."
fi

# ---------------------------------------------------------------------------
# Rimuove l'eventuale palette FurrOS scritta da versioni precedenti nel
# registro di LibreOffice (solo il blocco marcato, con backup).
# ---------------------------------------------------------------------------
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
if ! command -v thunar >/dev/null 2>&1; then
  echo "  Nota: Thunar non è installato; il tema resta attivo per le altre app GTK3."
fi
if [ -n "${LO_PRESENT:-}" ]; then
  case ":$PATH:" in
    *":$HOME_DIR/.local/bin:"*) ;;
    *)
      echo "  Nota: ~/.local/bin non è nel PATH."
      echo "  Le voci di menu usano il wrapper LibreOffice; da terminale usa:"
      echo "    $HOME_DIR/.local/bin/libreoffice"
      ;;
  esac
fi
echo "  LibreOffice usa il tema GTK precedente: $PREV_GTK"
echo "Verifica:"
echo "  gsettings get org.gnome.desktop.interface gtk-theme"
echo "  gsettings get org.gnome.desktop.interface icon-theme"
