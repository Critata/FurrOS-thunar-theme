#!/usr/bin/env bash
# Rimuove il tema FurrOS da LibreOffice ripristinando l'ultimo backup creato da install.sh.
set -euo pipefail

HOME_DIR="${HOME:-/home/$(id -un)}"

if pgrep -x soffice.bin >/dev/null 2>&1; then
  echo "Errore: chiudi tutti i documenti di LibreOffice prima di ripristinare." >&2
  exit 1
fi

shopt -s nullglob
for REG in "$HOME_DIR"/.config/libreoffice/*/user/registrymodifications.xcu; do
  BACKUPS=("$REG".bak-furros-*)
  if (( ${#BACKUPS[@]} == 0 )); then
    echo "Nessun backup FurrOS per $REG"
    continue
  fi
  LATEST="$(printf '%s\n' "${BACKUPS[@]}" | sort | tail -n1)"
  cp -a "$LATEST" "$REG"
  echo "  ripristinato $REG da $LATEST"
done

echo "Tema LibreOffice rimosso. I backup sono stati conservati."
