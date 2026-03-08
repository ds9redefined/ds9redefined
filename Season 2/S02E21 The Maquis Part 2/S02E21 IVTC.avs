input = LSMASHVideoSource("DS9_TheMaquisPt2.mov").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

RIFEConv = input.fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
DI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).TDecimate(mode=2, rate=23.976)

PD1 = inputDW.Pulldown(0, 2) 
PD2 = inputDW.Pulldown(0, 3)
PD3 = inputDW.Pulldown(1, 3)
PD4 = inputDW.Pulldown(1, 4)
PD5 = inputDW.Pulldown(2, 4)

Row1 = StackHorizontal(PD1, PD2, PD3)
Row2 = StackHorizontal(PD4, PD5, DIDraft)

PD1

ReplaceFramesSimple(PD2, "PD2Map.txt")
ReplaceFramesSimple(PD3, "PD3Map.txt")
ReplaceFramesSimple(PD4, "PD4Map.txt")
ReplaceFramesSimple(PD5, "PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "RIFEMap.txt")
RemapFrames(fileName="DIMap.txt", sourceClip=DI)

ReplaceFramesSimple(PD2.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).TDecimate(mode=2, rate=23.976), mappings="[58475 58734] [59461 59632] [60375 60688]")
ReplaceFramesSimple(PD3.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).TDecimate(mode=2, rate=23.976), mappings="[58844 58858] [58874 58884]")
ReplaceFramesSimple(PD4.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).TDecimate(mode=2, rate=23.976), mappings="[58735 58815] [58885 58942] [59759 59839]")
ReplaceFramesSimple(PD5.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).TDecimate(mode=2, rate=23.976), mappings="[59203 59207] [60856 61086]")

# DeRainbow
ASTDRmc(tempsoftsc=1)
