input = LSMASHVideoSource("DS9_TheMaquisPt2.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(75373, 75467)

input

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc(tempsoftsc=1)