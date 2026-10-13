LSMASHVideoSource("DS9_Wishes.mov").AssumeTFF().Crop(0, 6, 0, -2)
DoubleWeave()
Pulldown(1, 4)
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(50892, 50973)

