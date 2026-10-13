input = LSMASHVideoSource("DS9_ThePassenger_nn3D.mov").AssumeTFF().Crop(0, 6, 0, -2)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

Trim(129543, 129725)