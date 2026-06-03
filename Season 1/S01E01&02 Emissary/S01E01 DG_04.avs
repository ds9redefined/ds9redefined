input = AVISource("S01E01 IVTC.avs")

input

Trim(7140,  7202)

# DeRainbow
ASTDRmc()

# Deghosting
vsLGhost(mode=[1, 1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7, 8], intensity=[20, 25, 20, 15, 10, 5])
