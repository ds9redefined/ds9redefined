LSMASHVideoSource("DS9_ProfitandLoss.mov").AssumeTFF().Crop(0, 4, 0, -4).Trim(8550, 11910)

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

# DeRainbow
ASTDRmc(tempsoftsc=5)
