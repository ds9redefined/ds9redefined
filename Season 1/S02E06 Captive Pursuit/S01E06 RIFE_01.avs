input = LSMASHVideoSource("DS9_CaptivePursuit.mov").AssumeTFF().Crop(0, 6, 0, -2).Trim(25176, 25226)

input

# 30p to 24p interpolation
ConvertBits(32).ConvertToPlanarRGB().RIFE(model=65, fps_num=24000, fps_den=1001, gpu_thread=4).ConvertBits(10, dither=1).ConvertToYUV422()

#DeRainbow
ASTDRmc()
