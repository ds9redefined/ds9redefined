LSMASHVideoSource("DS9_PastPrologue.mov").Crop(0, 6, 0, -2)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])

Trim(163688, 165787)

ASTDRmc()
