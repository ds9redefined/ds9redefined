#Use in 480/60p version, mask in viewscreen

LSMASHVideoSource("DS9_PastPrologue.mov").AssumeTFF().Crop(0, 6, 0, -2)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

ASTDRmc(tempsoftsc=1)

Trim(16242, 16395)