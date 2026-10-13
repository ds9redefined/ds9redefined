LSMASHVideoSource("DS9_SecondSight_NTSCJ.mov").AssumeTFF().Crop(0, 6, 0, -2)

DoubleWeave()

Pulldown(1, 3)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(59424, 59515)