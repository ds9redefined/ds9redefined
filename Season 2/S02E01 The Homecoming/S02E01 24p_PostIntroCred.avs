AVISource("S02E01 IVTC.avs")

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[50, 20, 15, 10, 5])

Trim(11164, 12403)