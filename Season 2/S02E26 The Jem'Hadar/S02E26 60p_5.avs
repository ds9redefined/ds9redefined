LSMASHVideoSource("DS9_TheJemHadar.mov").AssumeTFF().Crop(0, 6, 0, -2)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

Trim(92780, 92809)