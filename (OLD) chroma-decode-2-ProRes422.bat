@echo off
:: Check if a file was dropped onto the .bat file
if "%~1"=="" (
    echo Please drag and drop a file onto this script.
    pause
    exit /b
)

:: Get the full path, filename without extension, and directory of the file
set "filepath=%~1"
set "filename=%~n1"
set "filedir=%~dp1"

:: Construct and execute the command
ld-chroma-decoder -f ntsc3d --luma-nr 0 --chroma-nr 0 --chroma-gain 1.25 --chroma-phase 0.0 -p y4m --input-json "%filedir%%filename%.tbc.json" "%filedir%%filename%.tbc" | ffmpeg -i - -c:v prores_ks -profile:v 3 -vendor ap10 -f mov -pix_fmt yuv422p10le -r 30000/1001 -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" "%filedir%%filename%.mov"
