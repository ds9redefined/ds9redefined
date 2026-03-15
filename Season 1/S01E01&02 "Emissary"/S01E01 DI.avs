input = LSMASHVideoSource("DS9_EmissaryPt1.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(15486, 15605)

input

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

vsLGhost(mode=[1, 1, 1, 1, 1, 1, 1], shift=[-4, -3, 3, 4, 5, 6, 7], intensity=[-5, -10, 25, 20, 15, 10, 5])