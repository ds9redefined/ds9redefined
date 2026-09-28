input = LSMASHVideoSource("DS9_CaptivePursuit.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(46752, 46788)

input

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#DeRainbow
ASTDRmc()
