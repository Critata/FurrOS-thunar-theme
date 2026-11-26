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

After changing the theme CSS, reload the theme and restart Thunar:

```bash
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
sleep 1
gsettings set org.gnome.desktop.interface gtk-theme 'FurrOS'
pkill -TERM thunar || true
setsid thunar --daemon >/dev/null 2>&1 &
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
| paper | `#FFECEC` | text, borders, file and drop-down menu text |
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
  paper text and no dark ink edge, so selected files never look dark; the
  font weight of the label is not changed on selection, so rows do not shift
  when highlighted. GTK's cell renderer uses `theme_unfocused_selected_bg_color`
  when the window loses focus, so the theme defines a doubled rosé value
  there: GTK blends it 50% with the view background, yielding exactly the
  same pink as the focused state instead of the inherited cyan accent.
  Switching tabs or windows therefore keeps the same pink selection and
  paper text. Thunar's `ExoIconView` adds the `.rubberband`
  class to the view itself, so the rule targets `.view.rubberband` with enough
  specificity to beat `.standard-view .view`; the dragged rectangle is a
  light translucent rosé tint with square corners and a 1 px opaque maroon
  frame. Both limits are imposed by `exo_icon_view_update_rubberband()`,
  which only invalidates a 1 px ring around the previous rectangle: a thicker
  frame or anti-aliased rounded corners leave stale pixels (artifacts) inside
  the new rectangle while dragging.
- The information area below the side-pane places uses translucent surfaces
  (`alpha(...)`) and 12 px rounded corners instead of the default grey box.
- Combo boxes and dropdown lists use one compact 22 px pill: night field and
  arrow cell, a continuous paper outline, cyan arrow and pink sticker shadow.
  The arrow stays inside the same pill instead of becoming a separate block.
  Combo popovers keep the `surface-2` background with a cyan border, and the
  selected row uses maroon with bold paper text for strong contrast.
- Spin buttons share the same pill treatment and keep their +/- controls
  centred and clickable inside it. Check and radio indicators get explicit
  icon sources because `adw-gtk3-dark` disables the inherited ones; compact
  icon-button metrics are scoped to sidebar headers. Focus rings are drawn
  inside the chip radius, so hover/active/checked states no longer leave
  double borders or paper-coloured residue outside the corners.
- Icons are scalable SVG and work at any size. `generate.py` needs only
  Python 3.
