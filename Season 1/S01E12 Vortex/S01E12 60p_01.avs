LSMASHVideoSource("DS9_Vortex.mov").AssumeTFF().Crop(0, 6, 0, -2)

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

Trim(90340, 90549)