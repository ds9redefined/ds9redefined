input = MPEG2Source("%source_file%").ConvertToYUV422()

# Use, rearrange, and modify as needed. This is mostly just to keep a record of the settings.

# De-interlaced 60p (for segments that still exhibit interlacing artifacts)
#deint = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# Inverse Telecine
#IVTC = input.TFM(cthresh=9, slow=2, pp=2, micmatching=3, clip2=input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, FPSDivisor=2)).TDecimate(sceneThresh=10, hybrid=0)

# Interpolate 30fps sections to 24fps. Use Trim(FirstFrame#, LastFrame#) to only interpolate and output that section. User ReplaceFramesSimple(mappings=[FirstFrame# LastFrame#]) to insert that section into the episode as a whole.
#RIFE = input.ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertBits(8, dither=1).ConvertToYUV422(matrix="601:l")

# DeRainbow
#IVTC.ASTDRmc()

# Deghosting (generated titles/credits in particular)
#vsLGhost(mode=[1, 1], shift=[3, 4], intensity=[30, 20])

# Dot Crawl Reduction
#QTGMC(Preset="Slower", InputType=1)

# Extreme Dot Crawl Reduction
#MCTemporalDenoise(settings="very high")

