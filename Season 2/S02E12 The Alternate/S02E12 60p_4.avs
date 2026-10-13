input = LSMASHVideoSource("DS9_TheAlternate.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(67316, 67424)

input

# Inverse Telecine

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, FPSDivisor=2)

# DeRainbow
ASTDRmc()
