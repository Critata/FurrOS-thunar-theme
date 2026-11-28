# FurrOS Thunar Theme

A GTK3/GTK4 theme for **Thunar** that reproduces the [FurrOS](https://furros.xyz/)
design system: dark surfaces, chunky sticker outlines, rounded chips, and
coordinated file/folder icons. LibreOffice is explicitly excluded so it keeps
the GTK theme that was active before FurrOS was installed.

No desktop screenshots are included in this repository.

> **Desktop support:** the most complete customization is currently available on
> KDE Plasma. The theme and icon set also work well on other desktops (GNOME,
> XFCE, ...), but fewer visual changes will be applied there.

## Contents

```
gtk3/                       GTK3 theme (adw-gtk3-dark/Adwaita + FurrOS overrides)
  gtk-3.0/gtk.css
  index.theme
gtk4/gtk-4.0/gtk.css        GTK4/libadwaita palette for Nautilus and GTK4 apps
icons/FurrOS-Papirus/       156 SVG icons (folders + file types)
  index.theme               inherits Papirus-Dark, Adwaita and hicolor
  generate.py               regenerates the icons
  scalable/places/
  scalable/mimetypes/
config/settings.ini.example reference values
install.sh                  install + backup + Thunar restart
uninstall.sh                restore the previous GTK theme and icons
```

## Install

On any GTK3 desktop with Thunar (tested on FurrOS/Arch and Zorin OS).
`adw-gtk3-dark` is used when present; otherwise the installer picks the system
GTK3 theme (Adwaita, Zorin, ...) so the FurrOS rules still apply.

```bash
git clone https://github.com/Critata/FurrOS-thunar-theme.git
cd FurrOS-thunar-theme
chmod +x install.sh uninstall.sh
./install.sh
```

The installer:

1. copies the theme to `~/.themes/FurrOS` and
   `~/.local/share/themes/FurrOS`;
2. copies the icons to `~/.local/share/icons/FurrOS-Papirus` and
   `~/.icons/FurrOS-Papirus`;
3. installs the GTK4 palette to `~/.config/gtk-4.0/gtk.css` (with a backup);
4. backs up `~/.config/gtk-3.0/settings.ini` and
   `~/.config/gtk-4.0/settings.ini` with a `.bak-DATE-TIME` suffix;
5. updates only the required keys (`gtk-theme-name`, `gtk-icon-theme-name`,
   Nunito font, dark mode), leaving the other settings untouched;
6. applies the same values through `gsettings`;
7. saves the current GTK theme and creates a LibreOffice wrapper plus local
   `.desktop` overrides, so LibreOffice keeps the previous theme;
8. removes an old FurrOS LibreOffice palette from the user registry, if any;
9. restarts Thunar if it was running.

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

This restores the GTK theme, icon theme, font and dark-mode preference saved by
`install.sh` (falling back to `adw-gtk3-dark`/`Adwaita` and
`Papirus-Dark` when no previous values exist), then removes the theme, icons,
GTK4 CSS, LibreOffice wrapper and local `.desktop` overrides. Backups created
by `install.sh` are kept.

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

- The CSS imports `adw-gtk3-dark` when it is available. `install.sh` rewrites
  the import to Adwaita on systems where only the stock GTK theme exists, so
  the FurrOS rules are not silently ignored on distributions such as Zorin OS.
- The theme is installed in both `~/.themes` and `~/.local/share/themes`, and
  the icon theme in both `~/.local/share/icons` and `~/.icons`, to cover the
  different lookup paths used by GTK3/GTK4 desktops.
- `gtk4/gtk-4.0/gtk.css` defines the libadwaita named colours
  (`window_bg_color`, `accent_bg_color`, `sidebar_bg_color`, ...). It is copied
  to `~/.config/gtk-4.0/gtk.css` so GTK4 apps such as GNOME Files/Nautilus use
  the same FurrOS palette as the GTK3 theme.
- LibreOffice is not themed by FurrOS. `install.sh` writes
  `~/.local/bin/furros-libreoffice`, which exports the GTK theme that was active
  before installation, and local `.desktop` overrides for Writer, Calc,
  Impress, Draw, Base, Math and the Start Center. GUI launches therefore use
  the previous theme. Native packages, Snap and Flatpak desktop files are
  supported. If `~/.local/bin` is in `PATH`, the `soffice`, `libreoffice` and
  `lo*` commands do too; otherwise use the menu entries or the wrapper path.
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
  Python 3. Archive file types reuse the normal folder silhouette with a
  zipper drawn down the front (teeth, slider and pull tab), so `.zip`, `.tar`,
  `.7z`, `.rar`, `.gz` and similar files read as folders instead of generic
  documents. Common folders (Documents, Downloads, Videos, Music, Pictures,
  Code, Games, Cloud, Recent, …) now use a large paper sticker with a drop
  shadow and a dedicated glyph — a page, a download arrow, a filmstrip, a
  note, a photo, brackets, a gamepad, etc. — plus a smaller paw watermark so
  it stays readable at 32 px. File icons also carry short labels
  (PDF, DOC, XLS, PPT, ODT, ODS, ODP, DOCX, XLSX, PPTX, PNG, JPG, SVG, GIF,
  WEBP, MP3, FLAC, WAV, OGG, MP4, MKV, WEBM, ISO, DEB, RPM, APK, APP, MD, PHP,
  RB, LUA, C#, DB, TOR, EPUB) and category glyphs for code, images, audio,
  video, spreadsheets, presentations, fonts and packages.
