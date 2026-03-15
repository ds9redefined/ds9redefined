input = AVISource("S01E01 IVTC.avs")

input

Trim(2033, 2284)

# Inverse Telecine
#TFM(cthresh=9, slow=2, pp=2, micmatching=3, clip2=input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, FPSDivisor=2)).TDecimate(sceneThresh=10, hybrid=0)

# DeRainbow
ASTDRmc()

# Deghosting
vsLGhost(mode=[1, 1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7, 8], intensity=[20, 25, 20, 15, 10, 5])
