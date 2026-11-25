# FurrOS Thunar Theme

A GTK3 theme for **Thunar** that reproduces the [FurrOS](https://furros.xyz/)
design system: dark surfaces, chunky sticker outlines, rounded chips, and
coordinated file/folder icons.

No desktop screenshots are included in this repository.

## Contents

```
gtk3/                       GTK3 theme (adw-gtk3-dark + FurrOS overrides)
  gtk-3.0/gtk.css
  index.theme
icons/FurrOS-Papirus/       65 SVG icons (folders + file types)
  index.theme               inherits from Papirus-Dark
  generate.py               regenerates the icons
  scalable/places/
  scalable/mimetypes/
config/settings.ini.example reference values
install.sh                  install + backup + Thunar restart
uninstall.sh                restore Adwaita / Papirus-Dark
```

## Install

On FurrOS/Arch with Thunar 4.20 and `adw-gtk3-dark` installed:

```bash
git clone https://github.com/Critata/FurrOS-thunar-theme.git
cd FurrOS-thunar-theme
chmod +x install.sh uninstall.sh
./install.sh
```

The installer:

1. copies the theme to `~/.themes/FurrOS`;
2. copies the icons to `~/.local/share/icons/FurrOS-Papirus`;
3. backs up `~/.config/gtk-3.0/settings.ini` and
   `~/.config/gtk-4.0/settings.ini` with a `.bak-DATE-TIME` suffix;
4. updates only the required keys (`gtk-theme-name`, `gtk-icon-theme-name`,
   Nunito font, dark mode), leaving the other settings untouched;
5. applies the same values through `gsettings`;
6. restarts Thunar if it was running.

Verify with:

```bash
gsettings get org.gnome.desktop.interface gtk-theme
gsettings get org.gnome.desktop.interface icon-theme
# 'FurrOS'
# 'FurrOS-Papirus'
```

## Uninstall

```bash
./uninstall.sh
```

This resets `gtk-theme` to `Adwaita` and `icon-theme` to `Papirus-Dark`, then
removes the theme and icons. Backups created by `install.sh` are kept.

## Palette

| Name | Colour | Used for |
| --- | --- | --- |
| night | `#150B11` | window and file-view background |
| plum | `#1E1218` | header bar, toolbar, side pane |
| surface | `#2A1A22` | panels |
| surface-2 | `#3A2430` | hovers and buttons |
| paper | `#FFECEC` | text, borders, selection |
| ink | `#0E080B` | shadows and text on paper |
| cyan | `#7FF0F0` | focus and primary accent |
| pink | `#FF8CBE` | secondary accent |
| red | `#E23A44` | shadows and destructive actions |
| maroon | `#781C2C` | hover state and folder backs |

## Implementation notes

- The CSS imports `/usr/share/themes/adw-gtk3-dark/gtk-3.0/gtk.css` as a base.
  Install `adw-gtk3-dark` first if it is missing.
- Thunar exposes internal style classes such as `.sidebar`, `.standard-view`,
  `.location-button` and `notebook`. They make it possible to style the side
  pane, file area, breadcrumbs and tabs without patching the application.
- There is deliberately **no image watermark behind file names**: the file
  view only has a very light dot texture, so selection stays readable.
- The information area below the side-pane places uses translucent surfaces
  (`alpha(...)`) and 12 px rounded corners instead of the default grey box.
- Combo boxes and dropdown lists (for example LibreOffice's font picker) are
  styled as one pill: transparent inner entry, cyan arrow, plum popover and
  cyan selected rows with a pink sticker shadow. Both GTK list-box and
  tree-view popups are covered.
- LibreOffice compatibility: toolbar buttons stay flat, comboboxes and dialog
  buttons use tighter padding/margins, and dialog surfaces have 14 px rounded
  corners. This avoids the inflated, overlapping widgets caused by the
  sticker shadows when used outside Thunar.
- Icons are scalable SVG and work at any size. `generate.py` needs only
  Python 3.
