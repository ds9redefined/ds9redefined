input = LSMASHVideoSource("DS9_RulesOfAcquisition_NTSCJ.mov").AssumeTFF().Crop(0, 6, 0, -2)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1], shift=[3, 4], intensity=[30, 20])

Trim(162056, 164755)