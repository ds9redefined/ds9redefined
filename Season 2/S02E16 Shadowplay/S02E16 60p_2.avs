LSMASHVideoSource("DS9_Shadowplay.mov").AssumeTFF().Crop(0, 6, 0, -2)

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()

Trim(88554, 88813)