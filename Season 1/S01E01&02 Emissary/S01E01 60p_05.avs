input = LSMASHVideoSource("DS9_EmissaryPt1.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(15250, 15383)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()
