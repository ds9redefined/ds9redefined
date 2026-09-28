AVISource("S01E07 IVTC.avs")

#Deinterlace
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1], shift=[3, 4], intensity=[30, 20])

Trim(65307, 65365)