input = LSMASHVideoSource("DS9_CaptivePursuit.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(10772,10861)

input

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1], shift=[4], intensity=[30])
