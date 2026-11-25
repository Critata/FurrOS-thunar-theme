#!/usr/bin/env bash
# Applica la palette FurrOS alla configurazione di LibreOffice (solo profilo utente).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"

python3 "$ROOT/generate.py"

shopt -s nullglob
REGISTRIES=("${HOME:-/home/$(id -un)}"/.config/libreoffice/*/user/registrymodifications.xcu)
if (( ${#REGISTRIES[@]} == 0 )); then
  echo "LibreOffice non trovato: nessun profilo utente da configurare."
  exit 0
fi

if pgrep -x soffice.bin >/dev/null 2>&1; then
  echo "Errore: chiudi tutti i documenti di LibreOffice prima di applicare il tema." >&2
  exit 1
fi

for REG in "${REGISTRIES[@]}"; do
  BACKUP="${REG}.bak-furros-${STAMP}"
  cp -a "$REG" "$BACKUP"
  echo "  backup: $BACKUP"

  python3 - "$REG" "$ROOT" <<'PY'
import re
import sys
from pathlib import Path

reg = Path(sys.argv[1])
root = Path(sys.argv[2])
text = reg.read_text(encoding="utf-8")

# Rimuove un'eventuale installazione precedente del tema.
block = re.compile(
    r"\s*<!-- FurrOS LibreOffice palette -->.*?"
    r"<!-- /FurrOS LibreOffice palette -->\s*",
    re.DOTALL,
)
text = block.sub("\n", text)

fragments = [
    (root / "settings.soc").read_text(encoding="utf-8"),
    (root / "dark-patch.soc").read_text(encoding="utf-8"),
    (root / "FurrOS.soc").read_text(encoding="utf-8"),
]
payload = ("\n<!-- FurrOS LibreOffice palette -->\n"
           + "\n".join(fragments)
           + "\n<!-- /FurrOS LibreOffice palette -->\n")

closing = "</oor:items>"
if text.rstrip().endswith(closing):
    idx = text.rfind(closing)
    text = text[:idx] + payload + text[idx:]
else:
    raise SystemExit(f"Formato inatteso in {reg}: manca {closing}")

reg.write_text(text, encoding="utf-8")
print(f"  aggiornato: {reg}")
PY
done

echo "Tema LibreOffice applicato. Riavvia LibreOffice per vedere i cambiamenti."
