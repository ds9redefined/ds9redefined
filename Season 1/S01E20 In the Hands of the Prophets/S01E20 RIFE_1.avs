LSMASHVideoSource("DS9_IntheHandsoftheProphets.mov").AssumeTFF().Crop(0, 6, 0, -2)

Trim(61173, 61368)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)
fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)

ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)
