input = LSMASHVideoSource("DS9_Tribunal.mov").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

inputDW.Pulldown(0, 3)

Trim(20959, 21303)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)