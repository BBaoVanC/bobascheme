# Color Research

I will attempt to keep a decent record of everything I looked up while
implementing the color space conversions.

In general, converting between color spaces involves first converting to the CIE
XYZ space, which is a description based on the amount of stimulation of the 3
different cone types we have, aka the three primary colors we perceive. X = red
(long), Y = green (medium), Z = blue (short). However, an important disadvantage
of XYZ is that it's not perceptually uniform. Equal distances in different parts
of the XYZ wheel don't correspond to colors that *feel* equally
different.[^cie1931]

There are perceptual color spaces that try to fix this, i.e. CIELAB and Oklab.
From a polar coordinate perspective, the radius is the intensity/saturation of
the color, the angle is the hue, and the third dimension is the lightness.
CIELAB is good, but there's a noticeable purple shift when you change the
lightness of a blue hue. Oklab is newer and fixes that issue; I think it's
supposed to be the preferred color space. It is the default color chooser space
in many programs such as Adobe Photoshop.

*Where is the center?* If we're talking polar coordinates, there has to be an
origin that everything radiates out from.

I based my colors originally off of CIELAB since that's what GIMP has built in.
I would like to migrate to Oklab in the future, but that requires a bit of
effort to pick colors I still like but are also at nice even positions.

[^cie1931]: [A Beginner’s Guide to (CIE) Colorimetry](https://medium.com/hipster-color-science/a-beginners-guide-to-colorimetry-401f1830b65a) and [CIE 1931 color space - Wikipedia](https://en.wikipedia.org/wiki/CIE_1931_color_space)

## Converting from LCH to LAB

This is simple. It's just a conversion from polar coordinates to rectangular.

## Converting from LAB to XYZ

The center point in the LAB space is the neutral, so the spot for pure
black/white/gray. But where in the XYZ space does this center point correspond
to? It depends on the chosen white point. This is usually the standard
illuminant D65.

I would like to give an intuitive/geometric explanation of these
transformations, but my linear algebra knowledge is not so great, so that might
be a bit risky.
