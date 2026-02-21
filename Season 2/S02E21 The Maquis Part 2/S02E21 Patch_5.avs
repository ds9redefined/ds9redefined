input = LSMASHVideoSource("DS9_TheMaquisPt2.mov").AssumeTFF().Crop(0, 6, 0, -2)

input

patch_top = SeparateFields().SelectEven().Trim(1, 0)
patch_bottom = SeparateFields().SelectOdd()
Interleave(patch_top, patch_bottom).Weave()

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").ConvertBits(10, dither=1)

ASTDRmc()

Trim(144698, 144737)

Pulldown(0, 2)