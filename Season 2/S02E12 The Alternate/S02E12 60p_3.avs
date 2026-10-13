input = LSMASHVideoSource("DS9_TheAlternate.mov").AssumeTFF().Crop(0, 6, 0, -2)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()

Trim(57268, 57720)