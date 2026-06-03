input = AVISource("S01E01 IVTC.avs")

input

Trim(8827, 9047)

# DeRainbow
ASTDRmc()

# Deghosting
vsLGhost(mode=[1, 1, 1, 1, 1, 1, 1, 1], shift=[-1, -2, 3, 4, 5, 6, 7, 8], intensity=[25, 20, 30, 30, 20, 15, 10, 5])
