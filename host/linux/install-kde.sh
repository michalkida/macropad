#!/bin/sh
# Install KDE Plasma global shortcuts for the macropad's Media page keys.
#   ./install-kde.sh             install (safe to re-run)
#   ./install-kde.sh --uninstall remove
#
# Each key gets a hidden .desktop launcher running macropad-media, bound
# through KWin's global shortcut service (same as System Settings >
# Shortcuts > Add Command, but scripted). Needs: wpctl, playerctl, gdbus.
set -eu

BIN="$HOME/.local/bin/macropad-media"
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

# Qt key codes: F19 = 0x01000042, F24 = 0x01000047, Shift modifier = 0x02000000
#        action        key code   name
ACTIONS="vol-min       16777282   Volume 0%
vol-max       16777287   Volume 100%
seek-back     50331714   Spotify seek back
seek-forward  50331719   Spotify seek forward"

accel() {
    gdbus call --session --dest org.kde.kglobalaccel --object-path /kglobalaccel \
        --method "org.kde.KGlobalAccel.$1" "$2" ${3:+"$3"} >/dev/null
}
# The KGlobalAccel calls take an action id: [component, action, component name, action name]

if [ "${1:-}" = "--uninstall" ]; then
    echo "$ACTIONS" | while read -r action key name; do
        accel unregister "macropad-$action.desktop" "_launch" || true
        rm -f "$APPS/macropad-$action.desktop"
    done
    rm -f "$BIN"
    kbuildsycoca6 >/dev/null 2>&1 || true
    echo "Removed macropad shortcuts."
    exit 0
fi

for tool in wpctl playerctl gdbus kbuildsycoca6; do
    command -v "$tool" >/dev/null || { echo "Missing $tool" >&2; exit 1; }
done

mkdir -p "$(dirname "$BIN")" "$APPS"
install -m 755 "$(dirname "$0")/macropad-media" "$BIN"

echo "$ACTIONS" | while read -r action key name; do
    cat > "$APPS/macropad-$action.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Macropad: $name
Exec=$BIN $action
NoDisplay=true
StartupNotify=false
X-KDE-GlobalAccel-CommandShortcut=true
EOF
done
kbuildsycoca6 >/dev/null 2>&1

echo "$ACTIONS" | while read -r action key name; do
    id="['macropad-$action.desktop', '_launch', 'Macropad: $name', 'Launch']"
    accel doRegister "$id"
    # Flags 6 = SetPresent | NoAutoloading: mark active (so KWin grabs the
    # key) and use this key rather than one loaded from config.
    gdbus call --session --dest org.kde.kglobalaccel --object-path /kglobalaccel \
        --method org.kde.KGlobalAccel.setShortcut "$id" "[$key]" 6 >/dev/null
    echo "Bound macropad-$action"
done
