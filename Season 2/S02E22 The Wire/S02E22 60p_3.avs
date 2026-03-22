LSMASHVideoSource("DS9_TheWire.mov").Crop(0, 6, 0, -2)

Trim(81034, 82830)

#Deinterlace
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc(tempsoftsc=1)

# Deghosting (generated titles/credits)
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])
