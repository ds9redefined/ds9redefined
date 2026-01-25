input = LSMASHVideoSource("DS9_TheMaquisPt1.mov").AssumeTFF().Crop(0, 4, 0, -4)

inputDW = input.DoubleWeave()

DIDraft = input.QTGMC(preset="draft").TDecimate(mode=2, rate=23.976)
RIFEConv = input.ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertToYUV422(matrix="601:l").ConvertBits(10, dither=1)
DI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).TDecimate(mode=2, rate=23.976)

PD1 = inputDW.Pulldown(0, 2) 
PD2 = inputDW.Pulldown(0, 3)
PD3 = inputDW.Pulldown(1, 3)
PD4 = inputDW.Pulldown(1, 4)
PD5 = inputDW.Pulldown(2, 4)

Row1 = StackHorizontal(PD1, PD2, PD3)
Row2 = StackHorizontal(PD4, PD5, DIDraft)

#StackVertical(Row1, Row2)

#Make interlacing easier to see
#Tweak(bright=-50, cont=3).Sharpen(1)

PD1

ReplaceFramesSimple(PD2, "PD2Map.txt")
ReplaceFramesSimple(PD3, "PD3Map.txt")
ReplaceFramesSimple(PD4, "PD4Map.txt")
ReplaceFramesSimple(PD5, "PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "RIFEMap.txt")
RemapFrames(fileName="DIMap.txt", sourceClip=DI)

# DeRainbow
ASTDRmc(tempsoftsc=1)