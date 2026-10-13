input = LSMASHVideoSource("DS9_Sanctuary_NTSCJ.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(53473, 53551)

input

# 30p to 24p interpolation
ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertBits(10, dither=1).ConvertToYUV422(matrix="601:l")

# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)
