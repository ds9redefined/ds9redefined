LSMASHVideoSource("DS9_PastPrologue.mov").AssumeTFF().Crop(0, 6, 0, -2)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

Trim(18890, 19082)

TDecimate(mode=2)

SelectOdd()

fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)