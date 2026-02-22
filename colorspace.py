"""
Implement color conversions, using CIE XYZ as an intermediate. Important for
converting Oklch colors to sRGB for programs that don't support directly
embedding oklab numbers in their configs.

Implement conversions OKLAB/OKLCH to/from sRGB, for programs that don't support
oklch numbers directly in their config files.

See https://bottosson.github.io/posts/oklab/#implementation
"""

from dataclasses import dataclass

@dataclass
class Oklch:
    """
    A color in the Oklab color space, written in terms of Lightness, Chroma,
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
        return f"oklch({self.L}, {self.C}, {self.h})"


@dataclass
class Oklab:
    """
    A color in the Oklab color space, in terms of lightness, and the two a/b
    opposing axes.
    """

    L: float
    a: float
    b: float
