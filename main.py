#!/usr/bin/env python3
"""
Generate bobascheme config files for programs based on templates
"""

from pathlib import Path
from string import Template

import colors
from colors import Color
from colorspace import *


def prepare_color_scheme_for_template(scheme: dict[colors.Color, Oklch]):
    colors_oklch = {
        "OKLCH__"+name.name: clr for name, clr in scheme.items()
    }
    return colors_oklch


if __name__ == "__main__":
    # The template file should be named whatever the specific program is. This
    # will become the dir name. The extension will be kept. Then inside the
    # dir, bobascheme_dark and bobascheme_light files will be created with that
    # kept extension.
    for theme in Path("./templates").iterdir():
        with open(Path("./templates")/theme.name, "r") as f:
            tmpl = Template(f.read())

        dest_dir = Path("./themes")/theme.stem
        dest_dir.mkdir(exist_ok=True)
        with open(dest_dir/("bobascheme_dark"+theme.suffix), "w+") as f:
            colors = prepare_color_scheme_for_template(colors.bobascheme_dark)
            f.write(tmpl.substitute(colors))
