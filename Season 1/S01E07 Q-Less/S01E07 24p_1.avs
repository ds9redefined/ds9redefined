input = LSMASHVideoSource("DS9_Qless.mov").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

inputDW.Pulldown(0, 2)

#DeRainbow
ASTDRmc()

Trim(58508, 58540)