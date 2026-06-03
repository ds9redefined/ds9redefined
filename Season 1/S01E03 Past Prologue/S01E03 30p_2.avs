#Use in 480/60p version, mask in just the window

LSMASHVideoSource("DS9_PastPrologue.mov").AssumeTFF().Crop(0, 6, 0, -2)

Trim(73298, 73453)