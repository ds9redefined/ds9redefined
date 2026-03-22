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
ffmpeg -y ^
  -i "%filedir%%filename%.mov" ^
  -c:v libx264 ^
  -profile:v high ^
  -b:v  1.5M ^
  -maxrate 3M ^
  -bufsize 6M ^
  -preset veryslow ^
  -tune film
  -pix_fmt yuv420p ^
  -aspect 4:3 ^
  -color_range tv ^
  -colorspace smpte170m ^
  -color_trc smpte170m ^
  -color_primaries smpte170m ^
  -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" ^
  -pass 1 ^
  -an ^
  -f null
  NUL

ffmpeg -y ^
  -i "%filedir%%filename%.mov" ^
  -c:v libx264 ^
  -profile:v high ^
  -b:v  1.5M ^
  -maxrate 3M ^
  -bufsize 6M ^
  -preset veryslow ^
  -tune film
  -pix_fmt yuv420p ^
  -aspect 4:3 ^
  -color_range tv ^
  -colorspace smpte170m ^
  -color_trc smpte170m ^
  -color_primaries smpte170m ^
  -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" ^
  -pass 2 ^
  "%filedir%%filename%.mp4"

echo.
echo Press any key to finish...
pause >nul
