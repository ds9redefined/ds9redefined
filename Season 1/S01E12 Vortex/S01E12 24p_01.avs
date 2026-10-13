LSMASHVideoSource("DS9_Vortex.mov").AssumeTFF().Crop(0, 6, 0, -2)

DoubleWeave()

Pulldown(2, 4)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(64069, 64168)