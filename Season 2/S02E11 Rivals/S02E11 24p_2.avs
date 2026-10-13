LSMASHVideoSource("DS9_Rivals.mov").AssumeTFF().Crop(0, 6, 0, -2)

DoubleWeave()

Pulldown(2, 4)

Trim(56888, 57043)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)
