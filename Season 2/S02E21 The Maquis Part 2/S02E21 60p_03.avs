input = LSMASHVideoSource("DS9_TheMaquisPt2.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(81567, 82913)

input

vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc(tempsoftsc=1)