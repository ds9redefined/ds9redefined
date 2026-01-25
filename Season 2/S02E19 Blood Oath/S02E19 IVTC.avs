input = LSMASHVideoSource("DS9_BloodOath.mov").AssumeTFF().Crop(0, 4, 0, -4)

inputDW = input.DoubleWeave()

PD1 = inputDW.Pulldown(0, 3) 
PD2 = inputDW.Pulldown(1, 4)
PD3 = inputDW.Pulldown(0, 2)
PD4 = inputDW.Pulldown(1, 3)
PD5 = inputDW.Pulldown(2, 4)

RIFEConv = input.ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertBits(10, dither=1).ConvertToYUV422(matrix="601:l")
DI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).AssumeFPS("ntsc_film")


PD3

ReplaceFramesSimple(PD2, "PD2Map.txt")
ReplaceFramesSimple(PD3, "PD3Map.txt")
ReplaceFramesSimple(PD4, "PD4Map.txt")
ReplaceFramesSimple(PD5, "PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "RIFEMap.txt")
RemapFrames(fileName="DIMap.txt", sourceClip=DI)

#Tweak(bright=50, cont=3)

# DeRainbow
#ASTDRmc(tempsoftsc=5)