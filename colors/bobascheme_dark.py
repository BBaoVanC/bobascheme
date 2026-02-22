from color import *
# 16 terminal colors

_hues = {
    "black": None,
    "red": 30,
    "green": 150,
    "yellow": 75,
    "blue": 250,
    "magenta": 330,
    "cyan": 200,
    "white": None,
}

_darks = {
    clr: Oklch(0.45, 0 if h is None else 0.13, h) for clr, h in _hues.items()
}
