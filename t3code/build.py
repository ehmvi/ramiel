#!/usr/bin/env python3
"""themes t3 code : une palette (palettes/*.css) -> un theme json t3 code.

memes roles que src/ramiel.css : fond surface, accent primary, core rare
(erreurs), ambre pour les avertissements, survols en teinte de primary.
t3 code veut des couleurs finies, donc les color-mix sont calcules ici
(oklab, comme dans le css).

    python3 t3code/build.py            # ecrit t3code/<id>.json
    t3 theme set t3code/ramiel.json    # publie et active (ou copier dans
                                       # ~/.t3/userdata/themes/)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VARIANTS = [
    {"id": "ramiel", "name": "ramiel", "palette": "palettes/ramiel.css"},
    {"id": "ramiel-orange", "name": "ramiel (orange)", "palette": "palettes/orange.css"},
]


def read_palette(path):
    text = (ROOT / path).read_text()
    return {k: v.lower() for k, v in re.findall(r"--m-([a-z-]+):\s*(#[0-9a-fA-F]{6})", text)}


# ---- oklab, pour reproduire color-mix(in oklab, ...) ----

def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _unlin(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def to_oklab(hex_):
    r, g, b = (_lin(int(hex_[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    )


def from_oklab(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )
    return "#" + "".join(f"{round(_unlin(c) * 255):02x}" for c in rgb)


def mix(base, other, amount):
    """color-mix(in oklab, base, other <amount>)"""
    p, q = to_oklab(base), to_oklab(other)
    return from_oklab(*(x + (y - x) * amount for x, y in zip(p, q)))


# ---- roles t3 code <- palette ----

def colors(p):
    """lisibilite d abord : fond releve d un cran (moins de halo autour du
    texte), texte un peu adouci (~11:1 au lieu de 14:1), texte secondaire et
    indications >= 4.5:1, bordures et panneaux assez marques pour lire la
    structure sans plisser les yeux."""
    lowest, surface, low = p["surface-lowest"], p["surface"], p["surface-low"]
    container, high, highest = p["surface-container"], p["surface-high"], p["surface-highest"]
    on_surface, on_variant = p["on-surface"], p["on-surface-variant"]
    outline, outline_variant = p["outline"], p["outline-variant"]
    primary, on_primary = p["primary"], p["on-primary"]
    core, ambre = p["core"], p["ambre"]

    # fonds : un cran au-dessus de la palette discord
    canvas = low
    sidebar = surface
    panel = mix(container, high, 0.5)
    raised = mix(high, highest, 0.5)

    # texte : entre on-surface et on-surface-variant, pas de blanc qui eblouit
    text = mix(on_surface, on_variant, 0.35)
    muted = mix(outline, on_variant, 0.25)       # secondaire, ~5.5:1
    hint = mix(outline_variant, outline, 0.85)   # indications, ~4:1

    # structure : bordures visibles mais douces
    border = mix(highest, outline_variant, 0.35)
    input_border = mix(outline_variant, outline, 0.25)

    # survols : teintes de primary, pas des aplats
    hover = mix(canvas, primary, 0.08)
    active = mix(canvas, primary, 0.16)
    side_hover = mix(sidebar, primary, 0.08)
    side_selected = mix(sidebar, primary, 0.16)
    side_active = mix(sidebar, primary, 0.24)

    return {
        # fondation
        "canvas": canvas,
        "chrome": canvas,
        "toolbar": canvas,
        "toolbarForeground": text,
        "toolbarBorder": border,
        "toolbarControl": panel,
        "toolbarControlForeground": text,
        "toolbarControlHover": active,
        "surface": panel,
        "surfaceRaised": raised,
        "surfaceOverlay": raised,
        "text": text,
        "textMuted": muted,
        "border": border,
        "input": input_border,
        # accent : primary
        "focus": primary,
        "accent": primary,
        "accentForeground": on_primary,
        "secondary": panel,
        "secondaryForeground": text,
        "muted": panel,
        "mutedForeground": muted,
        "placeholder": hint,
        "secondaryLabel": muted,
        "iconMuted": muted,
        "accentSurface": hover,
        "accentSurfaceForeground": p["on-primary-container"],
        # messages : bulle neutre, bouton d envoi en primary
        "messageSurface": panel,
        "messageForeground": text,
        "messageAction": primary,
        "messageActionForeground": on_primary,
        "messageActionHover": mix(primary, p["primary-container"], 0.25),
        # code en retrait, un cran plus sombre que le fond
        "codeBackground": surface,
        "codeForeground": text,
        # statuts : core pour les erreurs (rare), ambre pour avertir, tertiary pour les mises a jour
        "error": core,
        "errorForeground": mix(core, "#ffffff", 0.30),
        "errorSurface": mix(canvas, core, 0.14),
        "warning": ambre,
        "warningForeground": mix(ambre, "#ffffff", 0.18),
        "warningSurface": mix(canvas, ambre, 0.12),
        "update": p["tertiary"],
        "updateForeground": mix(p["tertiary"], "#ffffff", 0.15),
        "updateSurface": p["tertiary-container"],
        # recherche : comme la selection de texte, ambre pour le resultat courant
        "searchMatchBackground": p["primary-container"],
        "searchMatchForeground": p["on-primary-container"],
        "searchMatchActiveBackground": ambre,
        "searchMatchActiveForeground": lowest,
        # barre laterale : un cran plus sombre que le fond, survol en teinte de primary
        "sidebar": sidebar,
        "sidebarForeground": text,
        "sidebarMutedForeground": muted,
        "sidebarControlSurface": low,
        "sidebarRowHover": side_hover,
        "sidebarRowActive": side_active,
        "sidebarRowSelected": side_selected,
        "sidebarBorder": border,
        # terminal
        "terminalBackground": canvas,
        "terminalForeground": text,
        "terminalCursor": primary,
        "terminalSelection": p["primary-container"],
        "terminalScrollbar": highest,
        "terminalScrollbarHover": outline_variant,
    }


def main():
    out_dir = ROOT / "t3code"
    for v in VARIANTS:
        theme = {
            "version": 1,
            "name": v["name"],
            "appearance": "dark",
            "colors": colors(read_palette(v["palette"])),
        }
        path = out_dir / f"{v['id']}.json"
        path.write_text(json.dumps(theme, indent=2) + "\n")
        print(path.relative_to(ROOT), file=sys.stderr)


if __name__ == "__main__":
    main()
