AVISource("S02E22 IVTC.avs")

Trim(8300, 10007)

#Deinterlace
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2).SelectEven()

# DeRainbow
ASTDRmc(tempsoftsc=1)

# Deghosting (generated titles/credits)
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])
