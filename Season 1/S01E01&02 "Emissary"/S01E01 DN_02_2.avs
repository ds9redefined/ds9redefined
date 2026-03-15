input = AVISource("S01E01 IVTC.avs")

input

Trim(39473, 43850)

# DeRainbow
ASTDRmc()

# Extreme Dot Crawl Reduction
fmtc_bitdepth(8).ConvertToYV12().MCTemporalDenoise(settings="very high").ConvertToYUV422().fmtc_bitdepth(10)
