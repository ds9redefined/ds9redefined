LSMASHVideoSource("DS9_TheAlternate.mov").AssumeTFF().Crop(0, 6, 0, -2)

DoubleWeave()
Pulldown(1, 3)

# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(21695, 21788)