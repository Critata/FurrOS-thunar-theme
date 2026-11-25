#!/usr/bin/env python3
"""Generate the LibreOffice colour-scheme fragments for FurrOS.

LibreOffice 26.8 draws a large part of its UI itself (menu bar, menus,
sidebar, dialog controls, document background).  GTK CSS cannot reach those
surfaces, but LibreOffice exposes them as a colour scheme in its registry.
This script emits the XML fragments used by install.sh.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PALETTE = {
    "night":   "150B11",
    "plum":    "1E1218",
    "surface": "2A1A22",
    "surface2":"3A2430",
    "ink":     "0E080B",
    "paper":   "FFECEC",
    "dim":     "C8AAB4",
    "cyan":    "7FF0F0",
    "pink":    "FF8CBE",
    "red":     "E23A44",
    "maroon":  "781C2C",
    "green":   "78E6A0",
    "yellow":  "FFBE5A",
}

# LibreOffice colour-slot -> FurrOS palette entry.
SLOTS = {
    # Application chrome
    "WindowColor": "night",
    "WindowTextColor": "paper",
    "BaseColor": "plum",
    "ButtonColor": "surface",
    "ButtonTextColor": "paper",
    "AccentColor": "cyan",
    "DisabledColor": "surface2",
    "DisabledTextColor": "dim",
    "ShadowColor": "ink",
    "SeparatorColor": "maroon",
    "FaceColor": "plum",
    "ActiveColor": "cyan",
    "ActiveTextColor": "ink",
    "ActiveBorderColor": "pink",
    "FieldColor": "plum",
    "MenuBarColor": "night",
    "MenuBarTextColor": "paper",
    "MenuBarHighlightColor": "cyan",
    "MenuBarHighlightTextColor": "ink",
    "MenuColor": "plum",
    "MenuTextColor": "paper",
    "MenuHighlightColor": "cyan",
    "MenuHighlightTextColor": "ink",
    "MenuBorderColor": "maroon",
    "InactiveColor": "plum",
    "InactiveTextColor": "dim",
    "InactiveBorderColor": "surface2",
    # Document
    "DocColor": "surface",
    "DocBoundaries": "surface2",
    "AppBackground": "night",
    "TableBoundaries": "surface2",
    "FontColor": "paper",
    "Links": "cyan",
    "LinksVisited": "pink",
    "Spell": "red",
    "Grammar": "yellow",
    "SmartTags": "yellow",
    "Shadow": "ink",
    # Writer
    "WriterTextGrid": "surface2",
    "WriterBaselineGrid": "surface2",
    "WriterFieldShadings": "surface",
    "WriterIdxShadings": "surface",
    "WriterDirectCursor": "cyan",
    "WriterSectionBoundaries": "surface2",
    "WriterHeaderFooterMark": "dim",
    "WriterPageBreaks": "pink",
    "WriterNonPrintChars": "dim",
    # Calc
    "CalcGrid": "surface2",
    "CalcCellFocus": "cyan",
    "CalcPageBreak": "pink",
    "CalcPageBreakManual": "pink",
    "CalcPageBreakAutomatic": "dim",
    "CalcHiddenColRow": "surface2",
    "CalcTextOverflow": "red",
    "CalcComments": "yellow",
    "CalcDetective": "cyan",
    "CalcDetectiveError": "red",
    "CalcReference": "pink",
    "CalcNotesBackground": "plum",
    "CalcValue": "cyan",
    "CalcFormula": "yellow",
    "CalcText": "paper",
    "CalcProtectedBackground": "surface2",
    "DrawGrid": "surface2",
    # Basic IDE
    "BASICEditor": "night",
    "BASICIdentifier": "paper",
    "BASICComment": "dim",
    "BASICNumber": "yellow",
    "BASICString": "green",
    "BASICOperator": "pink",
    "BASICKeyword": "cyan",
    "BASICError": "red",
    # SQL
    "SQLIdentifier": "paper",
    "SQLNumber": "yellow",
    "SQLString": "green",
    "SQLOperator": "pink",
    "SQLKeyword": "cyan",
    "SQLParameter": "pink",
    "SQLComment": "dim",
    # HTML source
    "HTMLSGML": "cyan",
    "HTMLComment": "dim",
    "HTMLKeyword": "pink",
    "HTMLUnknown": "paper",
}

VISIBLE = {"Links", "LinksVisited", "DocBoundaries", "TableBoundaries",
           "Shadow", "WriterFieldShadings", "WriterIdxShadings",
           "WriterDirectCursor", "WriterSectionBoundaries", "DrawGrid"}


def value(slot):
    return int(PALETTE[SLOTS[slot]], 16)


def scheme_items(scheme):
    lines = [f'<item oor:path="/org.openoffice.Office.UI/ColorScheme/ColorSchemes">',
             f'  <node oor:name="{scheme}" oor:op="replace">']
    for slot in SLOTS:
        lines.append(f'    <node oor:name="{slot}">')
        lines.append(f'      <prop oor:name="Color" oor:op="fuse"><value>{value(slot)}</value></prop>')
        if slot in VISIBLE:
            lines.append('      <prop oor:name="IsVisible" oor:op="fuse"><value>true</value></prop>')
        lines.append('    </node>')
    lines.append('  </node>')
    lines.append('</item>')
    return "\n".join(lines)


def appearance_items():
    return "\n".join([
        '<item oor:path="/org.openoffice.Office.Common/Appearance">',
        '  <prop oor:name="LibreOfficeTheme" oor:op="fuse"><value>1</value></prop>',
        '  <prop oor:name="ApplicationAppearance" oor:op="fuse"><value>2</value></prop>',
        '  <prop oor:name="UseOnlyWhiteDocBackground" oor:op="fuse"><value>false</value></prop>',
        '  <prop oor:name="UseBmpForAppBack" oor:op="fuse"><value>false</value></prop>',
        '</item>',
        '<item oor:path="/org.openoffice.Office.UI/ColorScheme">',
        '  <prop oor:name="CurrentColorScheme" oor:op="fuse"><value>COLOR_SCHEME_LIBREOFFICE_DARK</value></prop>',
        '</item>',
        '<item oor:path="/org.openoffice.Office.Common/Misc">',
        '  <prop oor:name="SymbolStyle" oor:op="fuse"><value>sifr_dark</value></prop>',
        '  <prop oor:name="UseSystemFileDialog" oor:op="fuse"><value>true</value></prop>',
        '</item>',
    ])


def main():
    (ROOT / "dark-patch.soc").write_text(
        scheme_items("COLOR_SCHEME_LIBREOFFICE_DARK") + "\n", encoding="utf-8")
    (ROOT / "FurrOS.soc").write_text(
        scheme_items("FurrOS") + "\n", encoding="utf-8")
    (ROOT / "settings.soc").write_text(appearance_items() + "\n", encoding="utf-8")
    print("generated dark-patch.soc, FurrOS.soc, settings.soc")


if __name__ == "__main__":
    main()
