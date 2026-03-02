#!/usr/bin/env python3
"""
Generate bobascheme config files for programs based on templates
"""

from pathlib import Path
from string import Template

import colors
from colors import Color
from colorspace import *


def prepare_cielch_for_template(scheme: dict[colors.Color, CIELCh]):
    colors_cielch = {
        "CIELCH__"+k.name: v for k, v in scheme.items()
    }
    colors_hex = {
        "HEX__"+k.name: format(int(sRGB.convert(v)), '06x') for k, v in scheme.items()
    }
    return colors_cielch | colors_hex


if __name__ == "__main__":
    color_variables = prepare_cielch_for_template(colors.bobascheme_dark)
    # The template file should be named whatever the specific program is. This
    # will become the dir name. The extension will be kept. Then inside the
    # dir, bobascheme_dark and bobascheme_light files will be created with that
    # kept extension.
    for template_path in Path("./templates").iterdir():
        theme_dest_fname = "bobascheme_dark"+template_path.suffix
        theme_dest_subdir = template_path.stem.replace("SLASH", "/")
        theme_dest = Path("./themes")/theme_dest_subdir/theme_dest_fname
        with open(template_path, "r") as f:
            tmpl = Template(f.read())

        theme_dest.parent.mkdir(parents=True, exist_ok=True)
        with open(theme_dest, "w+") as f:
            print(f"rendering {template_path} to {theme_dest}")
            f.write(tmpl.substitute(color_variables))
