LSMASHVideoSource("DS9_TheCircle_NTSCJ.mov").AssumeTFF().Crop(0, 6, 0, -2)

# Convert to de-interlaced 60p
#QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)
DoubleWeave()

# DeRainbow
ASTDRmc()

Trim(116194, 116309)

SelectEvery(116, 0, 1, 4, 7, 10, 12, 16, 18, 22, 24, 27, 30, 33, 36, 39, 41, 45, 47, 51, 53, 56, 59, 62, 64, 68, 70, 74, 76, 79, 82, 85, 87, 91, 93, 97, 99, 102, 105, 108, 110, 114)

DI = last.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

ReplaceFramesSimple(DI, mappings="[0 0]")

AssumeFPS(24000, 1001)
fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000*47, fps_den=1001*41).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
AssumeFPS(24000, 1001)