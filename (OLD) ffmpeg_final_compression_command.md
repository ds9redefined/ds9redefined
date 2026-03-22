# Standard Def
ffmpeg -i "Path/S##E## Episode Title SD (LD).mov" -profile:v high -pix_fmt yuv420p -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" -c:v libx264 -crf 16 -preset veryslow -tune film "Path/S##E## Episode Title SD (LD).mov SD (LD).mp4"

# High Def
ffmpeg -i "Path/S##E## Episode Title SD (LD).mov HD (LD).mov" -profile:v main -pix_fmt yuv420p -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" -c:v libx265 -crf 22.5 -preset medium -tune grain "Path/S##E## Episode Title SD (LD).mov HD (LD).mp4"
