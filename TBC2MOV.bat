@echo off

:: Change directory to the location of the dropped file
cd /d "%~dp1"
if errorlevel 1 (
    echo ERROR: Could not navigate to the file's directory.
    pause
    exit /b
)

echo =================================================
echo  Working Directory: %CD%
echo  Converting: %~nx1
echo =================================================
echo.

E:\tbc-tools\ld-chroma-decoder -f ntsc3d --adapt-threshold 0.1 --chroma-weight 2.0 --luma-nr 0 --chroma-nr 0 --chroma-gain 1.0 --chroma-phase 0.0 --ntsc-phase-comp -p y4m --input-json "%~nx1.json" "%~nx1" | ffmpeg -i - -c:v prores_ks -profile:v 3 -vendor ap10 -f mov -pix_fmt yuv422p10le -r 30000/1001 -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" "%~n1.mov"

echo.
echo =================================================
echo  Conversion finished!
echo  Output file: %~n1.mov
echo =================================================
echo.

pause