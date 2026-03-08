input = LSMASHVideoSource("DS9_TheMaquisPt2.mov").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

DIDraft = input.QTGMC(preset="draft").TDecimate(mode=2, rate=23.976).Subtitle("DI", align=3)

PD1 = inputDW.Pulldown(0, 2).Subtitle("PD1", align=7)
PD2 = inputDW.Pulldown(0, 3).Subtitle("PD2", align=8)
PD3 = inputDW.Pulldown(1, 3).Subtitle("PD3", align=9)
PD4 = inputDW.Pulldown(1, 4).Subtitle("PD4", align=1)
PD5 = inputDW.Pulldown(2, 4).Subtitle("PD5", align=2)

Row1 = StackHorizontal(PD1, PD2, PD3)
Row2 = StackHorizontal(PD4, PD5, DIDraft)

StackVertical(Row1, Row2)

#Make interlacing easier to see
#Tweak(bright=-50, cont=3)
Sharpen(1)
#Tweak(bright=50)
