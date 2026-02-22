from enum import Enum, auto

from colorspace import *

class Color(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

    FORE_BLACK = 8
    FORE_RED = 9
    FORE_GREEN = 10
    FORE_YELLOW = 11
    FORE_BLUE = 12
    FORE_MAGENTA = 13
    FORE_CYAN = 14
    FORE_WHITE = 15

    BG = auto()
    FG = auto()

    BG1 = auto()
    FG1 = auto()
    BG2 = auto()
    FG2 = auto()
    BG3 = auto()
    FG3 = auto()

    URL = auto()

    def __repr__(self):
        return "Colors." + self.name

    def __str__(self):
        return self.name

    def bg(self):
        """Convert ANSI color to the background variant of same hue"""
        if self.value > 15:
            raise ValueError(
                "Only ANSI 16 colors can be converted between fore/back-ground"
            )
        if self.value >= 8:
            return Color(self.value - 8)
        return self

    def fg(self):
        """Convert ANSI color to the foreground variant of same hue"""
        if self.value > 15:
            raise ValueError(
                "Only ANSI 16 colors can be converted between fore/back-ground"
            )
        if self.value >= 8:
            return self
        return Color(self.value + 8)


_hues = {
    Color.BLACK: None,
    Color.RED: 30,
    Color.GREEN: 150,
    Color.YELLOW: 75,
    Color.BLUE: 250,
    Color.MAGENTA: 330,
    Color.CYAN: 200,
    Color.WHITE: None,
}

_dark_bg = {
    clr: Oklch(L=0.45, C=0.13, h=h) for clr, h in _hues.items()
}
_dark_fg = {
    clr.fg(): Oklch(L=0.65, C=0.13, h=h) for clr, h in _hues.items()
}
_dark_misc = {

}
bobascheme_dark = _dark_bg | _dark_fg | _dark_misc

_light_bg = {
    clr: Oklch(L=0.75, C=0.13, h=h) for clr, h in _hues.items()
}
_light_fg = {
    clr.fg(): Oklch(L=0.55, C=0.13, h=h) for clr, h in _hues.items()
}
bobascheme_light = _light_bg | _light_fg
