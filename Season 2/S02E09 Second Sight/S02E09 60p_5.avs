input = LSMASHVideoSource("DS9_SecondSight_NTSCJ.mov").AssumeTFF().Crop(0, 6, 0, -2)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()

Trim(150854, 151173)