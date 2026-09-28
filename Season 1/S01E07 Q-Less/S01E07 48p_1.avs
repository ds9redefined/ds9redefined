input = LSMASHVideoSource("DS9_Qless.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(47743, 47797)

Top = input.SeparateFields().SelectEven().SelectEvery(5, 0, 2, 3, 4)
Bottom = input.SeparateFields().SelectOdd().SelectEvery(5, 0, 1, 2, 4)

Interleave(Top, Bottom)
Weave()

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#DeRainbow
#ASTDRmc()
