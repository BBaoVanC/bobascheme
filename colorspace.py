"""
Implement color conversions. Many of the programs I use don't support putting
LCH colors directly in their config files, so they must be converted to rgb
and/or hex first.
"""

from dataclasses import dataclass
import math
import numpy as np

@dataclass
class CIELCh:
    """
    A color in the CIELAB color space, written in terms of Lightness, Chroma,
    and Hue. This is just a polar version of the rectangular CIELAB space. It
    can be transformed exactly as such.
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
    opposing axes. The white point is D50; this is used when converting to XYZ.
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
        white = WhitePoint.D50()

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

        return CIEXYZ(X, Y, Z, WhitePoint.D50())

@dataclass
class Oklab:
    """
    Oklab is a more accurate model than CIELAB. Especially noticeable on blue,
    where on CIELAB there's a noticeable purple shift depending on lightness.
    Also, the math in Oklab is significantly simpler, and it uses D65 so no
    adaptation is needed.
    """

    L: float
    a: float
    b: float

    # https://bottosson.github.io/posts/oklab/#implementation
    M1_INV = np.linalg.inv(np.array([
        [ +0.8189330101, +0.0329845436, +0.0482003018 ],
        [ +0.3618667424, +0.9293118715, +0.2643662691 ],
        [ -0.1288597137, +0.0361456387, +0.6338517070 ],
    ]))
    M2_INV = np.linalg.inv(np.array([
        [ +0.2104542553, +1.9779984951, +0.0259040371 ],
        [ +0.7936177850, -2.4285922050, +0.7827717662 ],
        [ -0.0040720468, +0.4505937099, -0.8086757660 ],

    ]))
    def to_xyz(self):
        lms_prime = M2_INV @ np.array([self.L, self.a, self.b])
        lms = lms_prime ** 3
        xyz = M1_INV @ lms
        return CIEXYZ(*xyz)

@dataclass
class WhitePoint:
    """
    A reference white point stored in terms of CIE XYZ coordinates. This space
    has the same geometry as the CIEXYZ object but the coordinate is
    semantically the white point itself, rather than being a coordinate
    referenced around a certain white point.
    """

    X: float
    Y: float
    Z: float

    @classmethod
    def from_xyY(cls, x, y, Y):
        # This conversion is also taken from Wikipedia but I think you can
        # somehow derive it if you have more motivation than I do now.
        # https://en.wikipedia.org/wiki/CIE_1931_color_space#CIE_xyY_color_space
        X = Y / y * x
        Z = Y / y * (1 - x - y)
        return WhitePoint(X, Y, Z)

    @classmethod
    def D50(cls):
        """
        https://www.w3.org/TR/css-color-4/#d50
        """

        # D50 coordinates fetched from CSS standard
        # Those are given in xyY space, where Y is assumed 1. So we must
        # convert to XYZ.
        return WhitePoint.from_xyY(0.345700, 0.358500, 1)

    @classmethod
    def D65(cls):
        """
        https://www.w3.org/TR/css-color-4/#d65
        """
        return WhitePoint.from_xyY(0.312700, 0.329000, 1)


@dataclass
class CIEXYZ:
    """
    CIE XYZ coordinates, combined with a reference white point that coordinates
    are aligned against.

    https://en.wikipedia.org/wiki/CIE_1931_color_space

    ## Why do we need a white point here?

    XYZ coordinates are absolute, but that's the issue. A pure gray will have
    its X and Y positions wherever the white point is. Transforming between
    different color spaces requires you to know where this white point, so you
    know what central point to be stretching and transforming the space around.

    If I understand correctly, then the white point only matters when we want
    to reproduce the color. For the color to be perceived correctly in the
    context of the lighting that the eye is currently under, it has to be
    "adapted" so that the neutrals/grays are the same color that your eye has
    automatically color balanced to in the environment.

    For example, the numbers in the sRGB transformation matrix are written with
    the assumption of a D65 white point. So it will stretch everything around
    D65's axis as the center. But if your colors were transformed to XYZ
    assuming a D50 white point, like with CIELAB, then the grays will be along
    the D50 axis instead, and will get stretched away from the D65 point. If I
    understand correctly, this means all the colors will be tilted warmer.

    TLDR: the `white` property gives the coordinate of pure white, lying on the
    axis that human eyes will interpret as being neutral black/gray/white. This
    is needed for color space transformations to know the center point that
    should be unmodified, while everything else is stretched and transformed
    around it.
    """

    X: float
    Y: float
    Z: float
    white: WhitePoint

    # http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
    MA_BRADFORD = np.array([
        [  0.8951000,  0.2664000, -0.1614000, ],
        [ -0.7502000,  1.7135000,  0.0367000, ],
        [  0.0389000, -0.0685000,  1.0296000, ],
    ])
    MA_BRADFORD_INV = np.array([
        [  0.9869929, -0.1470543,  0.1599627 ],
        [  0.4323053,  0.5183603,  0.0492912 ],
        [ -0.0085287,  0.0400428,  0.9684867 ],
    ])

    def adapt_bradford(self, new_white: WhitePoint):
        """
        Chromatic adaptation: to transform the color to be against a new white
        point
        """
        # Bradford transform implemented using constants from Bruce Lindbloom:
        # http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
        white_src = np.array([self.white.X, self.white.Y, self.white.Z])
        white_dst = np.array([new_white.X, new_white.Y, new_white.Z])
        LMS_src = self.MA_BRADFORD @ white_src
        LMS_dst = self.MA_BRADFORD @ white_dst
        out = self.MA_BRADFORD_INV @ np.diag(LMS_dst / LMS_src) @ \
            self.MA_BRADFORD @ np.array([[self.X], [self.Y], [self.Z]])
        # convert from column vector to just a list
        out = out.flatten()
        return CIEXYZ(out[0], out[1], out[2], new_white)

@dataclass
class sRGB:
    """
    Represents a color in sRGB color space. When calling hex(), the R is placed
    in most significant position, and B in the least significant.

    The RGB values are float but should be in range [0, 255]
    """
    # TODO: should these instead be int, and use np.round inside from_xyz to
    # round at the very start?
    R: float
    G: float
    B: float

    def __post_init__(self):
        assert 0 <= self.R <= 255
        assert 0 <= self.G <= 255
        assert 0 <= self.B <= 255

    def __index__(self):
        return (round(self.R) * 2**16) + (round(self.G) * 2**8) + (round(self.B))

    MA = np.array([
        [ 3.2406255, -1.5372080, -0.4986286 ],
        [-0.9689307,  1.8757561,  0.0415175 ],
        [ 0.0557101, -0.2040211,  1.0569959 ],
    ])

    @classmethod
    def from_xyz(cls, xyz: CIEXYZ):
        xyz = xyz.adapt_bradford(WhitePoint.D65())
        # I have fetched matrix values from Wikipedia as the IEC standard costs money
        # https://en.wikipedia.org/wiki/SRGB#Primaries
        xyz = np.array([xyz.X, xyz.Y, xyz.Z])
        linear_rgb = cls.MA @ xyz
        # https://en.wikipedia.org/wiki/SRGB#Transfer_function_(%22gamma%22)
        def gamma(r):
            if r <= 0.0031308:
                return 12.92 * r
            else:
                return 1.055 * r**(1/2.4) - 0.055
        gamma = np.vectorize(gamma)
        rgb = gamma(np.clip(linear_rgb, 0.0, 1.0)) * 255
        return sRGB(*rgb)

    @classmethod
    def convert(cls, clr):
        # first, start converting the color in known ways towards XYZ
        if isinstance(clr, CIELCh):
            clr = clr.to_lab()
        if isinstance(clr, CIELAB):
            clr = clr.to_xyz()

        # if it wasn't able to get to XYZ, then that's an error
        if not isinstance(clr, CIEXYZ):
            raise NotImplementedError("Color needs to be CIEXYZ, which didn't \
                happen somehow; it is currently " + str(type(clr)))

        return sRGB.from_xyz(clr)
