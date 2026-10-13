LSMASHVideoSource("DS9_Wishes.mov").AssumeTFF().Crop(0, 6, 0, -2)
Trim(76362, 76488)

DoubleWeave()
SelectEvery(254, 1, 4, 7, 10, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 79, 82, 85, 88, 91, 94, 97, 100, 103, 107, 110, 113, 116, 119, 122, 125, 128, 131, 134, 138, 141, 144, 147, 150, 153, 156, 159, 162, 165, 169, 172, 175, 178, 181, 184, 187, 190, 193, 196, 200, 203, 206, 209, 212, 215, 218, 221, 224, 227, 231, 234, 237, 240, 243, 246, 249, 252 )
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)