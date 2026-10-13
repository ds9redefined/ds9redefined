input = LSMASHVideoSource("DS9_TheAlternate.mov").AssumeTFF().Crop(0, 6, 0, -2)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(54485, 54509)
