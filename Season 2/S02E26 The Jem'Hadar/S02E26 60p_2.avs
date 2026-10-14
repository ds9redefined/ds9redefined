AVISource("S02E26 IVTC.avs")

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])

ASTDRmc()

Trim(65250, 65308)