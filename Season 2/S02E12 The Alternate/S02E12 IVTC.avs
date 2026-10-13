input = LSMASHVideoSource("DS9_TheAlternate.mov").AssumeTFF().Crop(0, 6, 0, -2)

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
434 
IVTCDI = last.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)
ReplaceFramesSimple(IVTCDI, "IVTCDIMap.txt")

# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

RIFEGen = AVISource("S02E12 RifeGen.avs")
ReplaceFramesSimple(RIFEGen, "RIFEGenMap.txt")

chroma = ConvertBits(8).checkmate(thr=1, max=1, tthr2=0)
luma = ConvertBits(8).checkmate(thr=0, max=1, tthr2=0)
decheck = luma.MergeChroma(chroma)
DN = decheck.ConvertToYV12().MCTemporalDenoise(settings="very high").ConvertToYUV422().ConvertBits(10)
ReplaceFramesSimple(DN, mappings="[36180 36274]")