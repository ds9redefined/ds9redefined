@echo off
setlocal enabledelayedexpansion

:: This loop processes every file dropped onto the batch icon
for %%A in (%*) do (
    
    echo -------------------------------------------------
    echo  Target: %%~nxA
    
    :: 'pushd' handles network paths and drive changes better than 'cd'
    pushd "%%~dpA"
    
    echo  Working in: !CD!
    
    :: Run ffmpeg using the filename only since we are now in the correct folder
    ffmpeg -i "%%~nxA" -c:v prores_ks -profile:v 3 -vendor ap10 -f mov -pix_fmt yuv422p10le -sws_flags "spline+accurate_rnd+full_chroma_int+full_chroma_inp" "%%~nA.mov"

    :: Return to the original starting directory
    popd
    
    echo  Finished: %%~nA.mov
)

echo.
echo =================================================
echo  All tasks complete.
echo =================================================
pause