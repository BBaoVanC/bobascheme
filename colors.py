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


# these were for oklch, maybe keep for future use
#_hues = {
#    Color.BLACK: None,
#    Color.RED: 30,
#    Color.GREEN: 150,
#    Color.YELLOW: 75,
#    Color.BLUE: 250,
#    Color.MAGENTA: 330,
#    Color.CYAN: 200,
#    Color.WHITE: None,
#}

_hues = {
    #Color.BLACK: None,
    Color.RED: 30,
    Color.GREEN: 150,
    Color.YELLOW: 75,
    Color.BLUE: 270,
    Color.MAGENTA: 330,
    Color.CYAN: 211,
    Color.WHITE: None,
}

_dark_bg = {
    clr: CIELCh(L=45, C=50, h=h) for clr, h in _hues.items()
}
_dark_fg = {
    clr.fg(): CIELCh(L=65, C=50, h=h) for clr, h in _hues.items()
}
_dark_misc = {
    Color.BLACK: CIELCh(17.5, 0, None),
    Color.WHITE: CIELCh(77.3, 0, None),
    Color.FORE_BLACK: CIELCh(40, 0, None),
    Color.FORE_WHITE: CIELCh(92.5, 0, None),
    Color.URL:
}
bobascheme_dark = _dark_bg | _dark_fg | _dark_misc

#_light_bg = {
#    clr: Oklch(L=0.75, C=0.13, h=h) for clr, h in _hues.items()
#}
#_light_fg = {
#    clr.fg(): Oklch(L=0.55, C=0.13, h=h) for clr, h in _hues.items()
#}
#bobascheme_light = _light_bg | _light_fg
