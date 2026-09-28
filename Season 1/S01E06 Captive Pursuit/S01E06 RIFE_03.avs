input = LSMASHVideoSource("DS9_CaptivePursuit.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(46752, 46788)

input

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)

#DeRainbow
ASTDRmc()
