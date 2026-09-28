input = LSMASHVideoSource("DS9_CaptivePursuit.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(25778, 25919)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()
