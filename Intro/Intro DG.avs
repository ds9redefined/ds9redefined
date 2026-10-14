input = LSMASHVideoSource("DS9_ProfitandLoss.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(8550, 11910)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc(tempsoftsc=5)

vsLGhost(mode=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], shift=[-3, -4, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], intensity=[-10, -5, 20, 35, 20, 15, 10, 5, 4, 3, 2, 1])