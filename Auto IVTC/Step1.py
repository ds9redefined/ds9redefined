#!/usr/bin/env python3
"""
Step1.py

Sets up an episode folder: creates the AviSynth scripts and empty mapping
text files that Step2.py, Step3.py and the final encode need, with the
episode's MOV file and S##E## number filled in.

    1. Finds the .mov file in the folder (asks to confirm it, or to pick
       one when there are several).
    2. Takes the episode number (S##E##) from the folder path. The nearest
       folder that contains one wins, so a subfolder such as
       "S03E01 The Search Part 1\\LD" works.
    3. Writes the scripts below from the templates built into this file:
           S##E## DI.avs, S##E## IVTC.avs, S##E## RifeGen.avs,
           S##E## Mapping.avs, S##E## 60p_EndCred.avs,
           S##E## 24p_OutroCred.avs, S##E## 24p_PostIntroCred.avs,
           Scenes.avs
       If any of them already exist, asks once before overwriting them.
    4. Creates the empty text files below. Existing ones are never
       touched, since they may already hold work:
           Breaks.txt, DIMap.txt, IVTCDIMap.txt, PD2Map.txt, PD3Map.txt,
           PD4Map.txt, PD5Map.txt, RIFEGenMap.txt, RIFEMap.txt

Templates use {MOV} for the MOV file name and {EP} for S##E##.
"""

import argparse
import re
import sys
import traceback
from pathlib import Path


EPISODE_RE = re.compile(r"S\d{2}E\d{2}", re.IGNORECASE)

EMPTY_FILES = (
    "Breaks.txt",
    "DIMap.txt",
    "IVTCDIMap.txt",
    "PD2Map.txt",
    "PD3Map.txt",
    "PD4Map.txt",
    "PD5Map.txt",
    "RIFEGenMap.txt",
    "RIFEMap.txt",
)


# --------------------------------------------------------------------------
# AVS templates
# --------------------------------------------------------------------------

AVS_TEMPLATES = {
    "{EP} DI.avs": r'''LSMASHVideoSource("{MOV}").AssumeTFF().Crop(0, 6, 0, -2)

QTGMC(preset="draft")
''',

    "{EP} IVTC.avs": r'''input = LSMASHVideoSource("{MOV}").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

RIFEConv = input.fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
RIFEDI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2).fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
DI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

PD1 = inputDW.Pulldown(0, 2) 
PD2 = inputDW.Pulldown(0, 3)
PD3 = inputDW.Pulldown(1, 3)
PD4 = inputDW.Pulldown(1, 4)
PD5 = inputDW.Pulldown(2, 4)

PD1

ReplaceFramesSimple(PD2, "PD2Map.txt")
ReplaceFramesSimple(PD3, "PD3Map.txt")
ReplaceFramesSimple(PD4, "PD4Map.txt")
ReplaceFramesSimple(PD5, "PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "RIFEMap.txt")
RemapFrames(fileName="DIMap.txt", sourceClip=DI)

IVTCDI = last.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)
ReplaceFramesSimple(IVTCDI, "IVTCDIMap.txt")

# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

RIFEGen = AVISource("{EP} RifeGen.avs")
ReplaceFramesSimple(RIFEGen, "RIFEGenMap.txt")
''',

    "{EP} RifeGen.avs": r'''input = LSMASHVideoSource("{MOV}").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

RIFEConv = input.fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
RIFEDI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2).fmtc_bitdepth(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").fmtc_bitdepth(10)
DI = input.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

PD1 = inputDW.Pulldown(0, 2) 
PD2 = inputDW.Pulldown(0, 3)
PD3 = inputDW.Pulldown(1, 3)
PD4 = inputDW.Pulldown(1, 4)
PD5 = inputDW.Pulldown(2, 4)

PD1

ReplaceFramesSimple(PD2, "PD2Map.txt")
ReplaceFramesSimple(PD3, "PD3Map.txt")
ReplaceFramesSimple(PD4, "PD4Map.txt")
ReplaceFramesSimple(PD5, "PD5Map.txt")
ReplaceFramesSimple(RIFEConv, "RIFEMap.txt")
RemapFrames(fileName="DIMap.txt", sourceClip=DI)

IVTCDI = last.QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)
ReplaceFramesSimple(IVTCDI, "IVTCDIMap.txt")

# DeRainbow
ASTDRmc(tempsoftrad=1, tempsoftth=15, tempsoftsc=1)

z_ConvertFormat(pixel_type="RGBPS", colorspace_op="709:709:709:limited=>rgb:709:709:limited").ConvertToPlanarRGB()
RIFEGeneratedFrames(frameNumbers="RIFEGenMap.txt")
z_ConvertFormat(pixel_type="YUV422P10", colorspace_op="rgb:709:709:limited=>709:709:709:limited")''',

    "{EP} Mapping.avs": r'''input = LSMASHVideoSource("{MOV}").AssumeTFF().Crop(0, 6, 0, -2)

inputDW = input.DoubleWeave()

DIDraft = input.QTGMC(preset="draft").TDecimate(mode=2, rate=23.976).Subtitle("DI", align=3)
RIFEConv = input.ConvertBits(32).ConvertToPlanarRGB(matrix="601:l").RIFE(model=65, fps_num=24000, fps_den=1001).ConvertToYUV422(matrix="601:l").ConvertBits(10, dither=1)

PD1 = inputDW.Pulldown(0, 2).Subtitle("PD1", align=8).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD2 = inputDW.Pulldown(0, 3).Subtitle("PD2", align=8).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD3 = inputDW.Pulldown(1, 3).Subtitle("PD3", align=8).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD4 = inputDW.Pulldown(1, 4).Subtitle("PD4", align=8).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")
PD5 = inputDW.Pulldown(2, 4).Subtitle("PD5", align=8).ScriptClip("""subtitle(IsCombedTIVTC(4) ? "COMBED" : "CLEAN")""")

Row1 = StackHorizontal(PD1, PD2, PD3)
Row2 = StackHorizontal(PD4, PD5, DIDraft)

StackVertical(Row1, Row2)

#Make interlacing easier to see
#Tweak(bright=50, cont=3)
Sharpen(1)


''',

    "{EP} 60p_EndCred.avs": r'''input = LSMASHVideoSource("{MOV}").AssumeTFF().Crop(0, 6, 0, -2)

input

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1], shift=[3, 4], intensity=[30, 20])

#Trim()''',

    "{EP} 24p_OutroCred.avs": r'''AVISource("{EP} IVTC.avs")

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[45, 20, 15, 10, 5])

#Trim()''',

    "{EP} 24p_PostIntroCred.avs": r'''AVISource("{EP} IVTC.avs")

# Convert to de-interlaced 60p
QTGMC(Preset="Slower", SourceMatch=3, Lossless=2, fpsdivisor=2)

#DeRainbow
ASTDRmc()

#Deghosting (generated titles/credits in particular)
vsLGhost(mode=[1, 1, 1, 1, 1], shift=[3, 4, 5, 6, 7], intensity=[45, 20, 15, 10, 5])

#Trim()''',

    "Scenes.avs": r'''input = LSMASHVideoSource("{MOV}").AssumeTFF().Crop(0, 6, 0, -2)

DI = input.QTGMC(preset="draft").TDecimate(mode=2, rate=23.976)

DI

# source as 'last' (your QTGMC + TDecimate output)
global super = last.MSuper(pel=2, sharp=2)
global vec = MAnalyse(super, isb=false, blksize=16, delta=1)
global sc = MSCDetection(last, vec, thSCD1=400, thSCD2=130)

# sc is a clip where bright = scene change
ScriptClip(last, """
    score = AverageLuma(sc)
    score > 30 \
        ? Subtitle("Change " + String(score), size=48, text_color=$00FFFF00) \
        : Subtitle(String(score), size=24)
""")
''',
}


# --------------------------------------------------------------------------
# Prompts
# --------------------------------------------------------------------------

def ask(prompt: str) -> str | None:
    """input() that returns None instead of raising when stdin is closed."""
    try:
        return input(prompt).strip()
    except EOFError:
        print()
        return None


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = ask(prompt)
        if answer is None:
            return False
        answer = answer.lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter Y or N.")


def choose_mov(project_dir: Path) -> Path | None:
    """Return the MOV file to use, or None (after saying why) if there is
    none or the user declines."""
    movs = sorted((p for p in project_dir.iterdir()
                   if p.is_file() and p.suffix.lower() == ".mov"),
                  key=lambda p: p.name.lower())
    if not movs:
        print("No MOV file found.", file=sys.stderr)
        return None

    if len(movs) == 1:
        if ask_yes_no(f"MOV file {movs[0].name} found. Proceed? Y/N "):
            return movs[0]
        print("Cancelled.")
        return None

    print("Which MOV file?")
    for i, mov in enumerate(movs, start=1):
        print(f"  {i}. {mov.name}")
    while True:
        answer = ask(f"Enter a number (1-{len(movs)}): ")
        if answer is None:
            print("Cancelled.")
            return None
        if answer.isdigit() and 1 <= int(answer) <= len(movs):
            return movs[int(answer) - 1]
        print(f"Please enter a number from 1 to {len(movs)}.")


def wait_for_key() -> None:
    """Wait for a key press, so the window stays open when the script is
    launched by double-click."""
    print("Press any key to exit.")
    if not sys.stdin.isatty():
        return
    try:
        import msvcrt
        msvcrt.getch()
    except ImportError:
        input()


def finish(message: str) -> None:
    """Print the closing message and wait for a key press."""
    print()
    print(message)
    wait_for_key()


class _StderrCopy:
    """Passes stderr through while keeping a copy, so a failed run's error
    can be saved to a file."""

    def __init__(self, stream):
        self.stream = stream
        self.parts: list[str] = []

    def write(self, text):
        self.parts.append(text)
        return self.stream.write(text)

    def __getattr__(self, name):
        return getattr(self.stream, name)


def run_main() -> int:
    """Run main(). If it fails for any reason (an error it reports, an
    unexpected exception, or Ctrl+C), keep the window open and save the
    error to <script>_error.txt beside this script. A successful run
    removes that file."""
    script = Path(__file__).resolve()
    error_path = script.with_name(f"{script.stem}_error.txt")
    copy = _StderrCopy(sys.stderr)
    sys.stderr = copy
    try:
        code = main()
    except SystemExit as exc:      # argparse --help / usage errors
        code = exc.code if isinstance(exc.code, int) else (exc.code is not None)
    except BaseException:
        traceback.print_exc()
        code = 1
    finally:
        sys.stderr = copy.stream

    if not code:
        try:
            error_path.unlink()
        except FileNotFoundError:
            pass
        return 0

    print()
    error_text = "".join(copy.parts).strip()
    if error_text:
        try:
            error_path.write_text(error_text + "\n", encoding="utf-8")
            print(f"{script.name} did not finish. The error above was also "
                  f"saved to {error_path.name}.")
        except OSError:
            print(f"{script.name} did not finish.")
    else:
        print(f"{script.name} did not finish.")
    wait_for_key()
    return int(code)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def find_episode(project_dir: Path) -> str | None:
    """S##E## from the nearest folder in the path that has one."""
    for part in reversed(project_dir.parts):
        m = EPISODE_RE.search(part)
        if m:
            return m.group(0).upper()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--project-dir", type=Path,
                        default=Path(__file__).resolve().parent,
                        help="Episode folder with the .mov file "
                             "(default: script dir)")
    args = parser.parse_args()

    project_dir: Path = args.project_dir.resolve()

    episode = find_episode(project_dir)
    if episode is None:
        print(f"No episode number (S##E##) found in folder path: "
              f"{project_dir}", file=sys.stderr)
        return 1

    mov = choose_mov(project_dir)
    if mov is None:
        return 1
    print(f"Episode {episode}, source {mov.name}")
    print()

    scripts = {name.replace("{EP}", episode):
               text.replace("{MOV}", mov.name).replace("{EP}", episode)
               for name, text in AVS_TEMPLATES.items()}

    existing = [name for name in scripts if (project_dir / name).exists()]
    overwrite = True
    if existing:
        print("These scripts already exist:")
        for name in existing:
            print(f"  {name}")
        overwrite = ask_yes_no("Overwrite them? Y/N ")
        print()

    for name, text in scripts.items():
        path = project_dir / name
        if path.exists() and not overwrite:
            print(f"  kept:        {name}")
            continue
        status = "overwritten:" if path.exists() else "created:    "
        with path.open("w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(text)
        print(f"  {status} {name}")

    for name in EMPTY_FILES:
        path = project_dir / name
        if path.exists():
            print(f"  kept:        {name}")
            continue
        path.touch()
        print(f"  created:     {name}")

    finish("Use Scenes.avs to locate break frame numbers and add them to "
           "breaks.txt.")
    return 0


if __name__ == "__main__":
    sys.exit(run_main())
