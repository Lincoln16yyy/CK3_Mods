#!/usr/bin/env bash
# Installs (or reinstalls) the Smart Realm Director into the local CK3 mod folder.
#
#   ./tools/install.sh                 # auto-detect the CK3 user directory
#   ./tools/install.sh "/path/to/.../Paradox Interactive/Crusader Kings III"
#
# The script never touches saves, never edits vanilla files and never edits
# dlc_load.json: enable the mod in the launcher (or add "mod/Smart_Realm_Director.mod"
# to the enabled_mods list yourself).

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO/Smart_Realm_Director"

if [[ ! -d "$SRC" ]]; then
  echo "ERROR: $SRC not found" >&2
  exit 1
fi

if [[ $# -ge 1 ]]; then
  DEST="$1"
else
  mapfile -t CANDIDATOS < <(
    find "$HOME/.local/share/Paradox Interactive" \
         "$HOME/.config/hydralauncher/wine-prefixes" \
         "$HOME/Games/Heroic/Prefixes" \
         "$HOME/Games/umu" \
         -maxdepth 8 -type d -path "*Paradox Interactive/Crusader Kings III" 2>/dev/null | sort -u
  )
  if [[ ${#CANDIDATOS[@]} -eq 0 ]]; then
    echo "Could not find the CK3 user directory. Pass it as the first argument." >&2
    exit 1
  fi
  if [[ ${#CANDIDATOS[@]} -gt 1 ]]; then
    echo "More than one CK3 user directory found:" >&2
    printf '  %s\n' "${CANDIDATOS[@]}" >&2
    exit 1
  fi
  DEST="${CANDIDATOS[0]}"
fi

MODDIR="$DEST/mod"
mkdir -p "$MODDIR"

rm -rf "$MODDIR/Smart_Realm_Director"
cp -a "$SRC" "$MODDIR/"
cat > "$MODDIR/Smart_Realm_Director.mod" <<'EOF'
version="0.1.0"
tags={
	"Gameplay"
	"Utilities"
}
name="Smart Realm Director"
supported_version="1.20.*"
path="mod/Smart_Realm_Director"
EOF

echo "Installed into: $MODDIR/Smart_Realm_Director"
echo "Enable it in the launcher and keep it BELOW the automation mods listed in docs/MOD_COMPATIBILITY.md."
