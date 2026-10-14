input = LSMASHVideoSource("DS9_Crossover.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(81431, 82780)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

# Deghosting (generated titles/credits)
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])