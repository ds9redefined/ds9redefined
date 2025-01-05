# For ProRes 4444 output
ld-chroma-decoder -f ntsc3d --luma-nr 0 --chroma-nr 0 --chroma-gain 1.25 --chroma-phase 0.0 -p y4m --input-json "J:\S01E03 Past Prologue\LD\DS9_PastPrologue.tbc.json" "J:\S01E03 Past Prologue\LD\DS9_PastPrologue.tbc"| ffmpeg -i - -c:v prores_ks -profile:v 4 -vendor ap10 -f mov -pix_fmt yuv444p10le -r 30000/1001 -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" "J:\S01E03 Past Prologue\LD\DS9_PastPrologue.mov"

# For ProRes 422 output
ld-chroma-decoder -f ntsc3d --luma-nr 0 --chroma-nr 0 --chroma-gain 1.25 --chroma-phase 0.0 -p y4m --input-json "J:\S01E13 Battle Lines\LD\DS9_Battlelines.tbc.json" "J:\S01E13 Battle Lines\LD\DS9_Battlelines.tbc"| ffmpeg -i - -c:v prores_ks -profile:v 3 -vendor ap10 -f mov -pix_fmt yuv422p10le -r 30000/1001 -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" "J:\S01E13 Battle Lines\LD\DS9_Battlelines.mov"

# For FFV1 lossless output
ld-chroma-decoder -f ntsc3d --luma-nr 0 --chroma-nr 0 --chroma-gain 1.25 --chroma-phase 0.0 -p y4m --input-json "J:\S01E03 Past Prologue\LD\DS9_PastPrologue.tbc.json" "J:\S01E03 Past Prologue\LD\DS9_PastPrologue.tbc"| ffmpeg -i - -c:v ffv1 -level 3 -coder 1 -slices 4 -slicecrc 1 -pix_fmt yuv422p -r 30000/1001 -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" "J:\S01E03 Past Prologue\LD\DS9_PastPrologue.mkv"
