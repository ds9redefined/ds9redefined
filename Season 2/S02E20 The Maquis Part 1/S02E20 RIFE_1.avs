input = LSMASHVideoSource("DS9_TheMaquisPt1.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(9654, 9803)

input

# 30p to 24p interpolation
ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertBits(10, dither=1).ConvertToYUV422(matrix="601:l")

# DeRainbow
ASTDRmc()
