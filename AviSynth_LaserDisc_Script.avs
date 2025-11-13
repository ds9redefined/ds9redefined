input = LSMASHVideoSource("%source_file%").AssumeTFF().Crop(0, 4, 0, -4)

input

# Use, rearrange, and modify as needed

# Inverse Telecine
#TFM(cthresh=9, slow=2, pp=2, micmatching=3, clip2=input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, FPSDivisor=2)).TDecimate(sceneThresh=10, hybrid=0)

# De-interlaced 60p (for segments that still exhibit interlacing artifacts)
#QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# Interpolate 30fps sections to 24fps. Use Trim(FirstFrame#, LastFrame#) to only interpolate and output that section. User ReplaceFramesSimple(mappings=[FirstFrame# LastFrame#]) to insert that section into the episode as a whole.
#ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertBits(10, dither=1).ConvertToYUV422(matrix="601:l")

# DeRainbow
#Tweak(sat=2)
#ASTDRmc(tempsoftsc=1)
#Tweak(sat=.5)

# Deghosting (generated titles/credits in particular)
#vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[25, 20, 15, 10, 5])

# Dot Crawl Reduction
#QTGMC(Preset="Slower", InputType=1)

# Extreme Dot Crawl Reduction
#MCTemporalDenoise(settings="very high")

