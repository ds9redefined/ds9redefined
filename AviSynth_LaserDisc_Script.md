input = LSMASHVideoSource("%source_file%").AssumeTFF().Crop(0, 4, 0, -4).ConvertBits(8)

#De-interlaced 60p (for segments that still exhibit interlacing artifacts)
deint = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#Inverse Telecine
IVTC = input.TFM(cthresh=9, slow=2, pp=2, micmatching=3, clip2=input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, FPSDivisor=2)).TDecimate(sceneThresh=10, hybrid=0)

#Eliminate ntsc3d checkerboarding
chroma = IVTC.checkmate(thr=1, max=1, tthr2=0)
luma = IVTC.checkmate(thr=0, max=1, tthr2=0)
decheck = luma.MergeChroma(chroma)

#DeRainbow
decheck.ASTDRmc()

#Dot Crawl Reduction
#QTGMC(Preset="Slower", InputType=1)

#Extreme Dot Crawl Reduction
#MCTemporalDenoise(settings="very high")
