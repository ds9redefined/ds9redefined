input = LSMASHVideoSource("DS9_Dax.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(12747, 12803)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()
