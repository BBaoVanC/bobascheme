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
        # D50 coordinates fetched from CSS standard
        # https://www.w3.org/TR/css-color-4/#d50
        # These are given in xyY space, where Y is assumed 1. So we must
        # convert to XYZ.
        white_x = 0.345700
        white_y = 0.358500
        white_Y = 1
        # This conversion is also taken from Wikipedia but I think you can
        # somehow derive it if you have more motivation than I do now.
        # https://en.wikipedia.org/wiki/CIE_1931_color_space#CIE_xyY_color_space
        white_X = white_Y / white_y * white_x
        white_Z = white_Y / white_y * (1 - white_x - white_y)
        white = CIEXYZ(white_X, white_Y, white_Z)
        print(white)

        Lstar = self.L
        Astar = self.a
        Bstar = self.b
        # formulas from Wikipedia
        # https://en.wikipedia.org/wiki/CIELAB_color_space#From_CIELAB_to_CIEXYZ
        def finv(t):
            delt = 6/29
            if t > delt:
                return t**3
            else:
                return 3*(delt**2)*(t - 4/29)
        X = white.X * finv( (Lstar+16)/116 + (Astar/500) )
        Y = white.Y * finv( (Lstar+16)/116 )
        Z = white.Z * finv( (Lstar+16)/116 - (Bstar/200) )

        return CIEXYZ(X, Y, Z)

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
    def from_xyz(cls, xyz: CIEXYZ):
        # I have fetched matrix values from Wikipedia as the IEC standard costs money
        # https://en.wikipedia.org/wiki/SRGB#Primaries
        xyz = [xyz.X, xyz.Y, xyz.Z]
        print(xyz)
        primaries = {
            "R": [ 3.2406255, -1.5372080, -0.4986286 ],
            "G": [-0.9689307,  1.8757561,  0.0415175 ],
            "B": [ 0.0557101, -0.2040211,  1.0569959 ],
        }
        linear_rgb = {
            c: sum(map(lambda x: x[0] * x[1], zip(v, xyz))) for c, v in primaries.items()
        }
        print(linear_rgb)
        # https://en.wikipedia.org/wiki/SRGB#Transfer_function_(%22gamma%22)
        def gamma(r):
            if r <= 0.0031308:
                return 12.92 * r
            else:
                return 1.055 * r**(1/2.4) - 0.055
        def clamp(v):
            return max(v, 0, min(v, 1))
        # WIP: FIXME: the issue I am running into now is that LAB converted to
        # XYZ assuming a D50 white point, but sRGB assumes a D65 white point so
        # I guess it has to be converted somewhere along the line.
        #
        # The matrix multiplicaton part is working for sure, and I believe all
        # the RGB conversion to be also working correctly.
        rgb = { c: gamma(clamp(v)) * 255 for c, v in linear_rgb.items() }
        return sRGB(rgb["R"], rgb["G"], rgb["B"])

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
