input = LSMASHVideoSource("DS9_PlayingGod.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(77548, 77632)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()
