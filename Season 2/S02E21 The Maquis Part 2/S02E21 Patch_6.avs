input = LSMASHVideoSource("DS9_TheMaquisPt2.mov").AssumeTFF().Crop(0, 6, 0, -2)

input

DoubleWeave()

Pulldown(1, 3)

ASTDRmc(tempsoftsc=1)


Trim(62386, 62554)