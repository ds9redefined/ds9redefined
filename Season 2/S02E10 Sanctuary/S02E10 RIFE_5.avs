input = LSMASHVideoSource("DS9_Sanctuary_NTSCJ.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(76575, 76682)

input

# 30p to 24p interpolation
ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertBits(10, dither=1).ConvertToYUV422(matrix="601:l")

# DeRainbow
Tweak(sat=2)
ASTDRmc(tempsoftsc=1)
Tweak(sat=.5)
