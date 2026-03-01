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
    print("sdakjfasdf")
    print(sRGB.convert(scheme[colors.Color.RED]))
    colors_hex = {
        "HEX__"+k.name: format(int(sRGB.convert(v)), '06x') for k, v in scheme.items()
    }
    return colors_cielch | colors_hex


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
            # convert the defined CIELCH
            colors = prepare_cielch_for_template(colors.bobascheme_dark)
            f.write(tmpl.substitute(colors))
