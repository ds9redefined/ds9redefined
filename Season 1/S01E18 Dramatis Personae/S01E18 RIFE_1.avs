LSMASHVideoSource("DS9_DramatisPersonae.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(15214, 15224)

SeparateFields()
Top = last.SelectEven().Trim(3, 0)
Bottom = last.SelectOdd()

Interleave(Top, Bottom)
Weave()

SelectEvery(11, 0, 1, 2, 5, 6, 7, 9)

DI= last.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

RemapFrames(mappings="6 13", sourceClip=DI)

fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, factor_num=5, factor_den=3).AssumeFPS(24000, 1).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)