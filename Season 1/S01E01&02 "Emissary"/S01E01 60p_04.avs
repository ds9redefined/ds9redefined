input = LSMASHVideoSource("DS9_EmissaryPt1.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(9592, 9710)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()

vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])