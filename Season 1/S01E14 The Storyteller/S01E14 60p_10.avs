input = LSMASHVideoSource("DS9_TheStoryteller.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(77318, 77897)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)
#decheck = luma.MergeChroma(chroma)

#DeRainbow
ASTDRmc()

