input = LSMASHVideoSource("DS9_TheMaquisPt2.mov").AssumeTFF().Crop(0, 6, 0, -2)

input



#Patch for frames 42738-42845
patch_top = SeparateFields().SelectEven().Trim(1, 0)
patch_bottom = SeparateFields().SelectOdd()
Interleave(patch_top, patch_bottom).Weave()
#.DoubleWeave().Pulldown(1, 4)

QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)
#.TDecimate(mode=2, rate=23.976)

Trim(110250, 110287)

Pulldown(1, 4)

# DeRainbow
ASTDRmc(tempsoftsc=1)