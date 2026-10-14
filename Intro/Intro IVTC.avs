input = LSMASHVideoSource("DS9_ProfitandLoss.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(8550, 11910)

inputDW = input.DoubleWeave()

PD1 = inputDW.Pulldown(0, 3) 
PD2 = inputDW.Pulldown(1, 4)
PD3 = inputDW.Pulldown(0, 2)
PD4 = inputDW.Pulldown(1, 3)
PD5 = inputDW.Pulldown(2, 4)

PD3

ReplaceFramesSimple(PD1, mappings="[1159 1374]")
ReplaceFramesSimple(PD2, mappings="[1468 1662]")
#ReplaceFramesSimple(PD3, [1759 2689])

# DeRainbow
ASTDRmc(tempsoftsc=5)
