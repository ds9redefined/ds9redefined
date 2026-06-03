input = LSMASHVideoSource("DS9_EmissaryPt1_ntsc3D.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(56336, 56486)

input

# Inverse Telecine
#TFM(cthresh=9, slow=2, pp=2, micmatching=3, clip2=input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, FPSDivisor=2)).TDecimate(sceneThresh=10, hybrid=0)

# DeRainbow
ASTDRmc()
