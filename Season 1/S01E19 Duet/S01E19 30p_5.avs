LSMASHVideoSource("DS9_Duet.mov").AssumeTFF().Crop(0, 6, 0, -2)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

Trim(59965, 60170)