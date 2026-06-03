input = AVISource("S01E01 IVTC.avs")

input

Trim(7768, 7903)

# DeRainbow
ASTDRmc()

# Deghosting
vsLGhost(mode=[1, 1, 1, 1, 1, 1], shift=[-4, -2, 3, 4, 5, 6], intensity=[-10, 20, 25, 15, 10, 5])
