input = LSMASHVideoSource("DS9_Qless.mov").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

RIFEConv = input.fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
RIFEDI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2).fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
DI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

PD1 = inputDW.Pulldown(0, 2) 
PD2 = inputDW.Pulldown(0, 3)
PD3 = inputDW.Pulldown(1, 3)
PD4 = inputDW.Pulldown(1, 4)
PD5 = inputDW.Pulldown(2, 4)

PD1

ReplaceFramesSimple(PD2, "PD2Map.txt")
ReplaceFramesSimple(PD3, "PD3Map.txt")
ReplaceFramesSimple(PD4, "PD4Map.txt")
ReplaceFramesSimple(PD5, "PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "RIFEMap.txt")
RemapFrames(fileName="DIMap.txt", sourceClip=DI)
RemapFrames(mappings="[38194 38237] [0 43]", sourceClip=AviSource("S01E07 48p_1.avs"))

IVTCDI = last.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)
ReplaceFramesSimple(IVTCDI, "IVTCDIMap.txt")

# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)
