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
libreoffice/                LibreOffice application-colour palette
  generate.py               emits the registry fragments from the palette
  install.sh                patches the user profile (with backup)
  uninstall.sh              restores the last backup
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
6. installs the FurrOS colour scheme into the LibreOffice user profile when
   LibreOffice is closed (its registry is backed up first);
7. restarts Thunar if it was running.

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
removes the theme and icons. The LibreOffice palette is restored from its
backup as well. Backups created by `install.sh` are kept.

## Palette

| Name | Colour | Used for |
| --- | --- | --- |
| night | `#150B11` | window and file-view background |
| plum | `#1E1218` | header bar, toolbar, side pane |
| surface | `#2A1A22` | panels |
| surface-2 | `#3A2430` | hovers and buttons |
| paper | `#FFECEC` | text, borders, selected menu text |
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
- There is deliberately **no image watermark or texture behind file names**:
  the file view has a flat background, so translucent selection stays clean.
  File and side-pane selections use a light translucent rosé pink fill with
  paper text, which avoids the repaint glitches of a solid block; the font
  weight of the label is not changed on selection, so rows do not shift when
  highlighted. No outline radius is applied to selected items, so rubber-band
  dragging does not leave clipped artifacts. The mouse rubber-band itself uses
  an even lighter rosé tint so the dragged area stays transparent.
- The information area below the side-pane places uses translucent surfaces
  (`alpha(...)`) and 12 px rounded corners instead of the default grey box.
- Combo boxes and dropdown lists (for example LibreOffice's font picker) are
  styled as one pill: transparent inner entry, cyan arrow, and a `surface-2`
  popover that matches the arrow button's background. The list has a cyan
  border, and the selected row uses maroon with bold paper text for strong
  contrast. GTK list-box, tree-view and table popups are covered, including
  the dedicated `window.combo` that LibreOffice uses for its font selector.
  The arrow button keeps its native LibreOffice geometry and switches to cyan
  while the list is open.
- LibreOffice compatibility: toolbar buttons stay flat, comboboxes and dialog
  buttons use tighter padding/margins, and dialog surfaces have 14 px rounded
  corners. This avoids the inflated, overlapping widgets caused by the
  sticker shadows when used outside Thunar. The compact font is applied to the
  entire toolbar combobox, not just its inner entry, because LibreOffice can
  render labels such as "Preformatted Text" and "Liberation Mono" in a cell
  view; this keeps long values fully visible instead of clipped.
- LibreOffice 26.8 draws menus, the sidebar and the document background itself,
  so CSS alone cannot reach them. `libreoffice/` writes the FurrOS palette into
  the dark colour scheme in `registrymodifications.xcu`: night app background,
  surface-2 menus and list backgrounds, maroon menu selection with paper text,
  cyan menu borders, surface document pages and pink/maroon accents. It also
  selects the bundled `sifr_dark`
  icon set. Only the user profile is modified; no system files are touched.
- Icons are scalable SVG and work at any size. `generate.py` needs only
  Python 3.
