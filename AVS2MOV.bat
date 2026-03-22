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

ffmpeg -i "%~nx1" -c:v prores_ks -profile:v 3 -vendor ap10 -f mov -pix_fmt yuv422p10le -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" "%~n1.mov"

echo.
echo =================================================
echo  Conversion finished!
echo  Output file: %~n1.mov
echo =================================================
echo.

pause