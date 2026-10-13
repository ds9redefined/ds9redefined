LSMASHVideoSource("DS9_Progress.mov").AssumeTFF().Crop(0, 6, 0, -2)

DoubleWeave()
Pulldown(1, 4)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(5798, 5881)