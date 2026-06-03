AVISource("S01E04 IVTC.avs").Trim(7063, 9433)

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1], shift=[3, 4], intensity=[30, 20])
