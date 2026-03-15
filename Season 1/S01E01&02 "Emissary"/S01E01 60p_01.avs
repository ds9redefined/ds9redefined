input = LSMASHVideoSource("DS9_EmissaryPt1.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(1495, 1942)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc()

# Deghosting
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[-3, 3, 4, 5, 6], intensity=[-20, 25, 15, 10, 5])
