LSMASHVideoSource("DS9_Shadowplay.mov").AssumeTFF().Crop(0, 6, 0, -2)
DoubleWeave()
Pulldown(0, 2)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(13947, 14072)