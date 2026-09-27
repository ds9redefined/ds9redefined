input = AVISource("S01E05 IVTC.avs").Trim(65328, 65387)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7, 8], intensity=[25, 20, 15, 10, 5, 5])
