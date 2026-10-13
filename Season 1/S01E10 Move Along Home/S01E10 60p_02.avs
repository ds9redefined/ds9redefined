input = LSMASHVideoSource("DS9_MoveAlongHome.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(73553, 73753)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)
