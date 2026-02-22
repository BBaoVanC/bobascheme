"""
Implement color conversions, using CIE XYZ as an intermediate. Important for
converting Oklch colors to sRGB for programs that don't support directly
embedding oklab numbers in their configs.

Implement conversions OKLAB/OKLCH to/from sRGB, for programs that don't support
oklch numbers directly in their config files.

See https://bottosson.github.io/posts/oklab/#implementation
"""

class Oklch:
    """
    A color in the Oklab color space, written in terms of Lightness, Chroma,
    and Hue.
    """

    def __init__(self, l, c, h):
        self.lightness = l
        self.chroma = c
        self.hue = h


class Oklab:
    """
    A color in the Oklab color space, in terms of lightness, and the two a/b
    opposing axes.
    """

    def __init__(self, l, a, b):
        self.lightness = l
        self.a = a
        self.b = b
