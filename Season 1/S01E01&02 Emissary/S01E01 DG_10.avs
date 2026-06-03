input = AVISource("S01E01 IVTC.avs")

input

Trim(24396, 24508)

# DeRainbow
ASTDRmc()

# Deghosting
vsLGhost(mode=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], shift=[4, 5, 7, 8, 10, 11, 13, 14, 16, 17], intensity=[25, 25, 20, 20, 15, 15, 10, 10, 5, 5])

#tweak(bright=25, cont=2).sharpen(1)