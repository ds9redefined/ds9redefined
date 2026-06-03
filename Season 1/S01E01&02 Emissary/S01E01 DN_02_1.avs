input = AVISource("S01E01 IVTC.avs")

input

Trim(39473, 43850)

# DeRainbow
ASTDRmc()

# Eliminate ntsc3d checkerboarding
ConvertBits(8)
chroma = checkmate(thr=1, max=1, tthr2=0)
luma = checkmate(thr=0, max=1, tthr2=0)
luma.MergeChroma(chroma)
ConvertBits(10)
