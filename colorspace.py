"""
Implement color conversions, using CIE XYZ as an intermediate. Important for
converting Oklch colors to sRGB for programs that don't support directly
embedding oklab numbers in their configs.

Implement conversions OKLAB/OKLCH to/from sRGB, for programs that don't support
oklch numbers directly in their config files.

See https://bottosson.github.io/posts/oklab/#implementation
"""

from dataclasses import dataclass
import math

@dataclass
class CIELCh:
    """
    A color in the CIELAB color space, written in terms of Lightness, Chroma,
    and Hue.
    """

    L: float
    C: float
    h: float

    def __post_init__(self):
        if self.h == None:
            self.h = 0
            self.C = 0

    def __str__(self):
        return f"lch({self.L}, {self.C}, {self.h})"

    def to_lab(self):
        return CIELAB.from_lch(self)


@dataclass
class CIELAB:
    """
    A color in the CIELAB color space, in terms of lightness, and the two a/b
    opposing axes.
    """

    L: float
    a: float
    b: float

    @classmethod
    def from_lch(cls, lch: CIELCh):
        hue = math.radians(lch.h)
        return cls(
            lch.L,
            lch.C * math.cos(hue),
            lch.C * math.sin(hue),
        )

    def to_xyz(self):
        # These references from Wikipedia are for XYZ -> LAB
        # https://books.google.com/books?id=uZadszSGe9MC&q=lab+color+6-29+16-116&pg=PA61
        # https://web.archive.org/web/20191228145700/http://eilv.cie.co.at/term/157

        # D50 coordinates fetched from CSS standard
        # https://www.w3.org/TR/css-color-4/#d50
        white = CIEXYZ(0.345700, 0.358500, )

        Lstar = self.L
        Astar = self.a
        Bstar = self.b
        Xn = white.x
        Yn = white.y
        Zn = white.z
        # formulas from Wikipedia
        # https://en.wikipedia.org/wiki/CIELAB_color_space#From_CIELAB_to_CIEXYZ
        def finv(t):
            delt = 6/29
            if t > delt:
                return t**3
            else:
                return 3*(delt**2)*(t - 4/29)
        X = white.X
        raise NotImplementedError

@dataclass
class CIEXYZ:
    """
    https://en.wikipedia.org/wiki/CIE_1931_color_space
    """
    X: float
    Y: float
    Z: float

    #@classmethod
    #def from_xy(cls, x: float, y: float):
    #    return CIEXYZ(x, y, 1 - x - y)

@dataclass
class sRGB:
    """
    Represents a color in sRGB color space. WHen calling hex(), the R is placed
    in most significant position, and B in the least significant.
    """
    R: int
    G: int
    B: int

    def __post_init__(self):
        assert 0 <= self.R <= 255
        assert 0 <= self.G <= 255
        assert 0 <= self.B <= 255

    def __index__(self):
        return (self.R * 2**16) + (self.G * 2**8) + (self.B)

    @classmethod
    def from_xyz(cls, CIEXYZ):
        raise NotImplementedError

    @classmethod
    def convert(cls, clr):
        # first, start converting the color in known ways towards XYZ
        if isinstance(clr, CIELch):
            clr = clr.to_lab()
        if isinstance(clr, CIELAB):
            clr = clr.to_xyz()

        # if it wasn't able to get to XYZ, then that's an error
        if not isinstance(clr, CIEXYZ):
            raise NotImplementedError("Color needs to be CIEXYZ, which didn't \
                happen somehow; it is currently " + type(clr))

        return from_xyz(clr)
