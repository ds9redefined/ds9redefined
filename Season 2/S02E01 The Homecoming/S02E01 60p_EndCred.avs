input = LSMASHVideoSource("DS9_TheHomecoming_NTSCJ.mov").AssumeTFF().Crop(0, 4, 0, -4)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1], shift=[3, 4], intensity=[30, 20])

Trim(161924, 164623)