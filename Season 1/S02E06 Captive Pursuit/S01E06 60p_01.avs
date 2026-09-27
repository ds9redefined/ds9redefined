input = AVISource("S01E06 IVTC.avs")

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1, 1], shift=[3, 4, 5], intensity=[20, 20, 10])

Trim(8704, 10074)