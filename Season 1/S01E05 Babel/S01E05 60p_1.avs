input = AVISource("S01E05 IVTC.avs").Trim(10389, 12411)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7, 8], intensity=[30, 20, 20, 15, 10, 10])
