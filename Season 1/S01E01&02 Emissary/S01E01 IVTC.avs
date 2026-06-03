input = LSMASHVideoSource("DS9_EmissaryPt1.mov").AssumeTFF()

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

ReplaceFramesSimple(PD2, "1-PD2Map.txt")
ReplaceFramesSimple(PD3, "1-PD3Map.txt")
ReplaceFramesSimple(PD4, "1-PD4Map.txt")
ReplaceFramesSimple(PD5, "1-PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "1-RIFEMap.txt")
RemapFrames(fileName="1-DIMap.txt", sourceClip=DI)

#Opening Crawl
ReplaceFramesSimple(DI.fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10).vsLGhost(mode=[1, 1, 1, 1, 1], shift=[-3, 3, 4, 5, 6], intensity=[-20, 25, 15, 10, 5]), mappings="[1193 1554]")

#Single DI Frames
RemapFrames(mappings="3010 7526", sourceClip=DI_slow)

#Composited explosion and other stuff
ReplaceFramesSimple(DI_60.fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=73, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10), mappings="[7202 7288]")
ReplaceFramesSimple(DI_60.Pulldown(0, 2), mappings="[54330 54344]")
ReplaceFramesSimple(DI_60.Pulldown(0, 3), mappings="[39059 39131] [55748 55810]")
ReplaceFramesSimple(DI_60.Pulldown(1, 3), mappings="[7396 7670]")
ReplaceFramesSimple(DI_60.Pulldown(1, 4), mappings="[54157 54207]")

#Single Frame RIFE Replacements
fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l")
RIFEGeneratedFrames(frameNumbers="39219")
ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)

#DeFreq (scanline fix)
ReplaceFramesSimple(fmtc_bitdepth(8).defreq(fx=0, fy=50, dx=0, dy=2, sharp=0, info=false, show=0).fmtc_bitdepth(10), mappings="[1601 1748] [2475 2515] [2932 2988]")

#Deghosting
ReplaceFramesSimple(PD1.vsLGhost(mode=[1, 1, 1, 1, 1, 1], shift=[-4, -2, 3, 4, 5, 6], intensity=[-10, 20, 25, 15, 10, 5]), mappings="[7768 7903]")

Crop1 = Crop(0, 4, 0, -4)
Crop2 = Crop(0, 5, 0, -3)
Crop3 = Crop(0, 6, 0, -2)

Crop1

#White Line Fixes
ReplaceFramesSimple(Crop2, mappings="[43922 44078] [54305 54344]")
ReplaceFramesSimple(Crop3, mappings="[55637 56092]")

# DeRainbow
ASTDRmc(tempsoftsc=1)
