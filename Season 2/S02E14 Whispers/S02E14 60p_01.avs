LSMASHVideoSource("DS9_Whispers.mov").AssumeTFF().Crop(0, 6, 0, -2)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(30788, 31127)