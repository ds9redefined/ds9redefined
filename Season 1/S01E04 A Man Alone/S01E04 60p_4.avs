LSMASHVideoSource("DS9_AManAlone.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(2481, 2540)

SeparateFields()
Interleave(SelectEven().SelectEvery(5, 0, 1, 3, 4), SelectOdd().SelectEvery(5, 0, 1, 2, 3))
Weave()

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=60000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)