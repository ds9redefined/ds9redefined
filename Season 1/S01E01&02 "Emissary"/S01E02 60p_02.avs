input = LSMASHVideoSource("DS9_EmissaryPt2.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(74564, 74638)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()
