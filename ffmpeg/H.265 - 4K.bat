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
  -c:v libx265 ^
  -profile:v main10 ^
  -x265-params "level-idc=5.1" ^
  -b:v 75M ^
  -maxrate 100M ^
  -bufsize 200M ^
  -preset medium ^
  -tune grain ^
  -pix_fmt yuv420p10le ^
  -color_range tv ^
  -colorspace bt2020nc ^
  -color_trc bt709 ^
  -color_primaries bt2020 ^
  -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" ^
  -pass 1 ^
  -an ^
  -f null ^
  NUL

ffmpeg -y ^
  -i "%filedir%%filename%.mov" ^
  -c:v libx265 ^
  -profile:v main10 ^
  -x265-params "level-idc=5.1" ^
  -b:v 75M ^
  -maxrate 100M ^
  -bufsize 200M ^
  -preset medium ^
  -tune grain ^
  -pix_fmt yuv420p10le ^
  -color_range tv ^
  -colorspace bt2020nc ^
  -color_trc bt709 ^
  -color_primaries bt2020 ^
  -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" ^
  -pass 2 ^
  "%filedir%%filename%.mp4"

echo.
echo Press any key to finish...
pause >nul
