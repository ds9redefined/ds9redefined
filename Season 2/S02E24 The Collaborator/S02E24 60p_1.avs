AVISource("S02E24 IVTC.avs")

Trim(6445, 8415)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

# Deghosting (generated titles/credits)
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])
