input = LSMASHVideoSource("DS9_PastPrologue.mov").AssumeTFF().Crop(0, 4, 0, -4).ConvertBits(8).Trim(9409, 9600)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()
