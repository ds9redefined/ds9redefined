input = LSMASHVideoSource("DS9_Tribunal.mov").AssumeTFF().Crop(0, 6, 0, -2)

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

IVTCDI = last.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)
ReplaceFramesSimple(IVTCDI, "IVTCDIMap.txt")


# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

#ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")

z_ConvertFormat(pixel_type="RGBPS", colorspace_op="709:709:709:limited=>rgb:709:709:limited").ConvertToPlanarRGB()
RIFEGeneratedFrames(frameNumbers="10073 10084 [10090 10091] [10099 10101] [10110 10111] 10114 10118 10124 10132 [10136 10137] 10141 10148 10166 10301 10315 10541 10562 10566 10568 10631 10634 10666 10669 [10672 10674] 10680 10683 10687 10689 10692 10702 10728 [10744 10745] 10749 [10756 10757] [10761 10763] 10773 10784 10807 [10813 10814] 10825 10837 10850 10873 10900 10903 10909 [10926 10927] 10938 10943 [10963 10965] 10991 11043 11081 11087 11107 11114 11154 [11175 11177] [11180 11184] 11187 [11206 11210] 11223 11251 11256 [11259 11264] 11271 [11277 11278] [11282 11283] 11288 [11294 11299] 11304 11317 11324 [11328 11334] [11339 11341] [11345 11346]")
z_ConvertFormat(pixel_type="YUV422P10", colorspace_op="rgb:709:709:limited=>709:709:709:limited")

Trim(10069, 11348)