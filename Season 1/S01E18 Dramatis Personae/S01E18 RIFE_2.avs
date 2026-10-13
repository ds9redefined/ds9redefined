LSMASHVideoSource("DS9_DramatisPersonae.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(15398, 15414)


#SeparateFields()
#Top = last.SelectEven().SelectEvery(17, 0, 1, 2, 5, 6, 7, 9, 11, 12, 14, 15)
#Bottom = last.SelectOdd().SelectEvery(17, 0, 1, 2, 3, 4, 7, 8, 9, 11, 13, 14, 16)

#Interleave(Top, Bottom)
#Weave()

#DI= last.

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)
SelectEvery(34, 0, 1, 2, 3, 4, 5, 6, 8, 7, 10, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 19, 21, 22, 24, 23, 25, 26, 28, 27, 30, 32, 29, 31, 33)
SelectEvery(34, 0, 2, 4, 7, 9, 10, 14, 17, 19, 22, 23, 27, 29, 31, 33)
#fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, factor_num=13, factor_den=10).AssumeFPS(24000, 1).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)