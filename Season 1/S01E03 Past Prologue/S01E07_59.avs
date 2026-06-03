input = LSMASHVideoSource("..\..\S01E07 Q-Less\LD\DS9_Qless.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(76411, 76795)

input

DoubleWeave()
Pulldown(0, 2)

# Inverse Telecine
#TFM(cthresh=9, slow=2, pp=2, micmatching=3, clip2=input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, FPSDivisor=2)).TDecimate(sceneThresh=10, hybrid=0)

# DeRainbow
ASTDRmc()

#subtitle("Rec. 601", align=2)