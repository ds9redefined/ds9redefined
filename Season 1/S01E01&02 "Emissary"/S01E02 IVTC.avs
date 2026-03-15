input = LSMASHVideoSource("DS9_EmissaryPt2.mov").AssumeTFF()

inputDW = input.DoubleWeave()
RIFEConv = input.fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=73, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
DI_60 = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)
DI = DI_60.TDecimate(mode=2, rate=23.976)
DI_slow = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).AssumeFPS(24000, 1001)

PD1 = inputDW.Pulldown(0, 2)
PD2 = inputDW.Pulldown(0, 3)
PD3 = inputDW.Pulldown(1, 3)
PD4 = inputDW.Pulldown(1, 4)
PD5 = inputDW.Pulldown(2, 4)

PD1

ReplaceFramesSimple(PD2, "2-PD2Map.txt")
ReplaceFramesSimple(PD3, "2-PD3Map.txt")
ReplaceFramesSimple(PD4, "2-PD4Map.txt")
ReplaceFramesSimple(PD5, "2-PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "2-RIFEMap.txt")
RemapFrames(fileName="2-DIMap.txt", sourceClip=DI)

#Single DI Frames
RemapFrames(mappings="[4473 4564] [11185  11414]", sourceClip=DI_slow)

#Single Frame RIFE Replacements
fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l")
RIFEGeneratedFrames(frameNumbers="11912 34151")
ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)

#DeFreq (scanline fix)
#ReplaceFramesSimple(fmtc_bitdepth(8).defreq(fx=0, fy=50, dx=0, dy=2, sharp=0, info=false, show=0).fmtc_bitdepth(10), mappings="")



#Deghosting
#ReplaceFramesSimple(PD1.vsLGhost(mode=[1, 1, 1, 1, 1, 1], shift=[-4, -2, 3, 4, 5, 6], intensity=[-10, 20, 25, 15, 10, 5]), mappings="")

Crop1 = Crop(0, 4, 0, -4)
Crop2 = Crop(0, 5, 0, -3)
Crop3 = Crop(0, 6, 0, -2)

Crop1

#White Line Fixes
ReplaceFramesSimple(Crop2, mappings="")
ReplaceFramesSimple(Crop3, mappings="[53880 54025]")

# DeRainbow
ASTDRmc(tempsoftsc=1)

#Tweak(bright=50, cont=3)