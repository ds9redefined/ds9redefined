#!/usr/bin/env python3
"""
Step2.py  (formerly analyze_all.py)

Run after Step1.py has set up the folder and break frames have been added
to Breaks.txt.

Self-contained driver that produces frame_analysis.xlsx in one pass:

    Sheet 1 "Frame Analysis"  -- PD1..PD5 combed/clean status per frame
    Sheet 2 "Scene Ranges"    -- start/end frame pairs for each scene
                                 (scene changes + commercial-break starts
                                 from Breaks.txt are merged as splits)

Scene Ranges trimming (when Breaks.txt has entries):
  * Row 1 becomes 0 .. (first break - 1): everything before the episode
    proper is a single range; the scene ranges inside it are removed.
  * The row starting at the last break is extended to the final frame and
    every row after it is removed.
  * Column C = B - A (as a formula) for every row.
  * Rows whose range is shorter than 20 frames are highlighted light red
    (conditional formatting, so it tracks later edits).

AVS scripting (both passes are generated internally):
  * Source:          the `input = ...` line of Scenes.avs (written by
                     Step1.py), read at runtime.
  * Pulldown passes: combing checked with IsCombedTIVTC(4).
  * Scene pass:      on QTGMC + TDecimate output, two detectors whose
                     results are merged:
                       - MVTools MSCDetection, matching Scenes.avs
                         (MSuper/MAnalyse/MSCDetection then
                         AverageLuma > 30).
                       - Luma-difference spike: a frame whose
                         YDifferenceFromPrevious is at least 3x that of
                         both neighbouring frames (and at least 5, on an
                         8-bit scale). MSCDetection needs over half the
                         blocks to change, so it misses cuts in dark
                         scenes where black background matches black
                         background; the spike test catches those.
"""

import argparse
import bisect  # noqa: F401  (kept available for downstream tools)
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import PatternFill


# --- Pulldown phase constants ----------------------------------------------

PD_PARAMS = {
    "PD1": "0, 2",
    "PD2": "0, 3",
    "PD3": "1, 3",
    "PD4": "1, 4",
    "PD5": "2, 4",
}
COMBED_CTHRESH = 4  # IsCombedTIVTC threshold

# --- Scene-detection constants (mirror Scenes.avs) -------------------------

SCENE_SCORE_THRESHOLD = 30   # AverageLuma(sc) > 30 == scene change
MS_PEL = 2
MS_SHARP = 2
MA_BLKSIZE = 16
MA_DELTA = 1
MSCD_THSCD1 = 400
MSCD_THSCD2 = 130

# Luma-difference spike detector. Differences are on an 8-bit scale
# whatever the source bit depth. Tuned on S03E02: with MSCDetection it
# found 300 of 301 hand-confirmed cuts (MSCDetection alone: 266).
SPIKE_RATIO = 3.0        # diff must be >= this x both neighbours' diffs
SPIKE_MIN_DIFF = 5.0     # and at least this large
SPIKE_NEIGHBOUR_FLOOR = 0.125  # keeps near-static neighbours from dividing by ~0

# --- Sheet names -----------------------------------------------------------

SHEET1_NAME = "Frame Analysis"
SHEET2_NAME = "Scene Ranges"

# --- Short-range highlight (Scene Ranges) ---------------------------------

SHORT_RANGE_LENGTH = 20       # rows with B - A below this are highlighted
SHORT_RANGE_FILL = "FFC7CE"   # Excel's standard "Light Red Fill"
SHORT_RANGE_LAST_COL = "H"    # cover Step3.py's C..H columns too


# --------------------------------------------------------------------------
# Shared utilities
# --------------------------------------------------------------------------

def extract_input_line(avs_path: Path) -> str:
    """Return the first `input = ...` assignment line from the given AVS."""
    pattern = re.compile(r"^\s*input\s*=", re.IGNORECASE)
    with avs_path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            if pattern.match(raw):
                return raw.rstrip("\n")
    raise RuntimeError(f"Could not find 'input = ...' line in {avs_path}")


def _count_lines(path: Path) -> int:
    try:
        with path.open("rb") as fh:
            return sum(1 for _ in fh)
    except FileNotFoundError:
        return 0


def run_avs(runner_template: list[str], avs_path: Path, cwd: Path,
            log_path: Path, label: str, poll_interval: float = 0.2) -> None:
    """Run the AVS through the configured runner; show a live frame counter."""
    avs_str = str(avs_path)
    if any("{AVS}" in tok for tok in runner_template):
        cmd = [tok.replace("{AVS}", avs_str) for tok in runner_template]
    else:
        cmd = runner_template + [avs_str]

    proc = subprocess.Popen(
        cmd, cwd=str(cwd),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )

    use_cr = sys.stdout.isatty()
    last_count = -1
    try:
        while proc.poll() is None:
            count = _count_lines(log_path)
            if count != last_count:
                msg = f"[{label}] frame {count}"
                if use_cr:
                    sys.stdout.write("\r" + msg + " " * 8)
                else:
                    sys.stdout.write(msg + "\n")
                sys.stdout.flush()
                last_count = count
            time.sleep(poll_interval)
    finally:
        _, stderr = proc.communicate()

    final = _count_lines(log_path)
    end_msg = f"[{label}] frame {final} (done)"
    if use_cr:
        sys.stdout.write("\r" + end_msg + " " * 8 + "\n")
    else:
        sys.stdout.write(end_msg + "\n")
    sys.stdout.flush()

    if proc.returncode != 0:
        raise RuntimeError(
            f"AVS runner failed for {avs_path.name}\n"
            f"cmd: {' '.join(cmd)}\n"
            f"stderr:\n{stderr}"
        )


def default_runner() -> list[str]:
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", "{AVS}", "-f", "null", "-",
    ]


def parse_runner(value: str) -> list[str]:
    return value.split()


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
# Pulldown phase
# --------------------------------------------------------------------------

def build_pd_script(input_line: str, pd_args: str, log_path: Path) -> str:
    """One AVS per PD variant; writes 'frame,flag' per output frame."""
    log_str = str(log_path).replace("\\", "/")
    return (
        f"{input_line}\n"
        f"inputDW = input.DoubleWeave()\n"
        f"clip = inputDW.Pulldown({pd_args})\n"
        f'WriteFile(clip, "{log_str}", "current_frame", """ "," """, '
        f'"IsCombedTIVTC({COMBED_CTHRESH}) ? 0 : 1", '
        f'append=false, flush=true)\n'
    )


def parse_pd_log(log_path: Path) -> dict[int, int]:
    """Parse 'frame,flag' lines into {frame_index: 0|1}."""
    results: dict[int, int] = {}
    with log_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 2:
                continue
            try:
                frame = int(parts[0])
                flag = int(parts[1])
            except ValueError:
                continue
            results[frame] = flag
    return results


# --------------------------------------------------------------------------
# Scenes phase
# --------------------------------------------------------------------------

def build_scenes_script(input_line: str, log_path: Path,
                        score_threshold: int) -> str:
    """Generate AVS mirroring Scenes.avs (MSCDetection-based) but with
    WriteFile producing 'frame,is_scene_change,luma_diff' lines.
    luma_diff is YDifferenceFromPrevious scaled to 8-bit (0 on frame 0)."""
    log_str = str(log_path).replace("\\", "/")
    return (
        f"{input_line}\n"
        f'DI = input.QTGMC(preset="draft").TDecimate(mode=2, rate=23.976)\n'
        f"DI\n"
        f"global super = last.MSuper(pel={MS_PEL}, sharp={MS_SHARP})\n"
        f"global vec = MAnalyse(super, isb=false, "
        f"blksize={MA_BLKSIZE}, delta={MA_DELTA})\n"
        f"global sc = MSCDetection(last, vec, "
        f"thSCD1={MSCD_THSCD1}, thSCD2={MSCD_THSCD2})\n"
        f"global diff_scale = Pow(2, BitsPerComponent(last) - 8)\n"
        f'clip = ScriptClip(last, """\n'
        f"    global cur_score = AverageLuma(sc)\n"
        f"    global cur_diff = current_frame > 0 ? "
        f"YDifferenceFromPrevious() / diff_scale : 0.0\n"
        f'""")\n'
        f'WriteFile(clip, "{log_str}", "current_frame", """ "," """, '
        f'"cur_score > {score_threshold} ? 1 : 0", """ "," """, '
        f'"cur_diff", append=false, flush=true)\n'
    )


def parse_scenes_log(log_path: Path) -> tuple[dict[int, int],
                                                 dict[int, float]]:
    """Parse 'frame,flag,diff' lines into ({frame: flag}, {frame: diff})."""
    flags: dict[int, int] = {}
    diffs: dict[int, float] = {}
    with log_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 3:
                continue
            try:
                frame = int(parts[0])
                flag = int(parts[1])
                diff = float(parts[2])
            except ValueError:
                continue
            flags[frame] = flag
            diffs[frame] = diff
    return flags, diffs


def find_spikes(diffs: dict[int, float], ratio: float) -> list[int]:
    """Frames whose luma difference from the previous frame stands out
    against both neighbouring frames' differences (a hard cut)."""
    spikes: list[int] = []
    for frame, d in diffs.items():
        if d < SPIKE_MIN_DIFF:
            continue
        prev_d = diffs.get(frame - 1)
        next_d = diffs.get(frame + 1)
        if prev_d is None or next_d is None:
            continue
        if d >= ratio * max(prev_d, next_d, SPIKE_NEIGHBOUR_FLOOR):
            spikes.append(frame)
    return sorted(spikes)


def load_breaks(breaks_path: Path) -> list[int]:
    """Frame numbers (one per line) from Breaks.txt; blanks and #-comments
    ignored. Non-integer lines are skipped with a warning."""
    if not breaks_path.exists():
        return []
    frames: list[int] = []
    with breaks_path.open("r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                frames.append(int(line))
            except ValueError:
                print(f"WARNING: Breaks.txt line {lineno}: ignoring "
                      f"non-integer value {line!r}", file=sys.stderr)
    return frames


# --------------------------------------------------------------------------
# Workbook builders
# --------------------------------------------------------------------------

def populate_frame_analysis(ws, pd_results: dict[str, dict[int, int]]) -> None:
    """Sheet 1: Frame, PD1..PD5. Row 1 is the header."""
    ws.cell(row=1, column=1, value="Frame")
    for col_idx, pd_name in enumerate(PD_PARAMS, start=2):
        ws.cell(row=1, column=col_idx, value=pd_name)

    if not any(pd_results.values()):
        return

    max_frame = max(max(r.keys()) for r in pd_results.values() if r)
    for frame in range(max_frame + 1):
        row = frame + 2
        ws.cell(row=row, column=1, value=frame)
        for col_idx, pd_name in enumerate(PD_PARAMS, start=2):
            ws.cell(row=row, column=col_idx,
                    value=pd_results[pd_name].get(frame))


def populate_scene_ranges(ws, scenes: list[int], breaks: list[int],
                          last_frame: int) -> None:
    """Sheet 2: 0-based ranges, A1 = 0. Breaks merge in as additional
    range starts identical in role to scene changes."""
    valid_breaks = [b for b in breaks if 0 < b <= last_frame]
    dropped = len(breaks) - len(valid_breaks)
    if dropped:
        print(f"WARNING: {dropped} break frame(s) outside valid range "
              f"(1..{last_frame}) were ignored", file=sys.stderr)

    all_splits = sorted(set(scenes) | set(valid_breaks))

    starts = [0] + all_splits
    ends = [sc - 1 for sc in all_splits] + [last_frame]
    ranges = [[a, b] for a, b in zip(starts, ends)]

    if valid_breaks:
        # Row 1 covers everything before the first break; drop the scene
        # ranges that fall inside it.
        first_break = min(valid_breaks)
        head = [0, first_break - 1]
        ranges = [head] + [r for r in ranges if r[0] >= first_break]

        # The row starting at the last break runs to the final frame; drop
        # every row after it.
        last_break = max(valid_breaks)
        idx = next(i for i, r in enumerate(ranges) if r[0] == last_break)
        ranges[idx][1] = ranges[-1][1]
        del ranges[idx + 1:]

    for row, (a, b) in enumerate(ranges, start=1):
        ws.cell(row=row, column=1, value=a)
        ws.cell(row=row, column=2, value=b)
        ws.cell(row=row, column=3, value=f"=B{row}-A{row}")

    # Light-red rows where the range is short. Tests B - A directly rather
    # than column C, since Step3.py later overwrites column C.
    fill = PatternFill(start_color=SHORT_RANGE_FILL, end_color=SHORT_RANGE_FILL,
                       fill_type="solid")
    ws.conditional_formatting.add(
        f"A1:{SHORT_RANGE_LAST_COL}{len(ranges)}",
        FormulaRule(formula=[f"$B1-$A1<{SHORT_RANGE_LENGTH}"], fill=fill),
    )


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--project-dir", type=Path,
                        default=Path(__file__).resolve().parent,
                        help="Folder with Scenes.avs / Breaks.txt "
                             "(default: script dir)")
    parser.add_argument("--xlsx", type=Path, default=None,
                        help="Output workbook "
                             "(default: <project>/frame_analysis.xlsx)")
    parser.add_argument("--runner", type=parse_runner, default=None,
                        help='AVS runner with {AVS} placeholder, e.g. '
                             '"ffmpeg -hide_banner -loglevel error -y -i {AVS} '
                             '-f null -"')
    parser.add_argument("--scene-threshold", type=int,
                        default=SCENE_SCORE_THRESHOLD,
                        help=f"AverageLuma(sc) > N triggers a scene change "
                             f"(default: {SCENE_SCORE_THRESHOLD})")
    parser.add_argument("--spike-ratio", type=float, default=SPIKE_RATIO,
                        help=f"Luma-difference spike needed for a cut, as a "
                             f"multiple of both neighbouring frames' "
                             f"differences; 0 turns the spike detector off "
                             f"(default: {SPIKE_RATIO})")
    parser.add_argument("--breaks", type=Path, default=None,
                        help="Path to Breaks.txt "
                             "(default: <project>/Breaks.txt)")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep generated AVS and log files for inspection")
    args = parser.parse_args()

    project_dir: Path = args.project_dir.resolve()
    scenes_avs = project_dir / "Scenes.avs"
    if not scenes_avs.exists():
        print(f"Missing required AVS: {scenes_avs} (run Step1.py first)",
              file=sys.stderr)
        return 1

    xlsx_path: Path = (args.xlsx or project_dir / "frame_analysis.xlsx").resolve()
    runner_cmd = args.runner or default_runner()

    input_line = extract_input_line(scenes_avs)

    # ---- Phase 1: Pulldown analysis (5 PD passes) ----
    pd_results: dict[str, dict[int, int]] = {}
    temp_files: list[Path] = []
    try:
        for pd_name, pd_args in PD_PARAMS.items():
            avs_file = project_dir / f"_analysis_{pd_name}.avs"
            log_file = project_dir / f"_analysis_{pd_name}.log"
            if log_file.exists():
                log_file.unlink()
            avs_file.write_text(
                build_pd_script(input_line, pd_args, log_file),
                encoding="utf-8",
            )
            temp_files.extend([avs_file, log_file])

            run_avs(runner_cmd, avs_file, cwd=project_dir,
                    log_path=log_file, label=pd_name)
            if not log_file.exists():
                raise RuntimeError(
                    f"No log produced for {pd_name}; AVS likely did not "
                    f"process any frames."
                )
            pd_results[pd_name] = parse_pd_log(log_file)

        # ---- Phase 2: Scene analysis (single pass) ----
        sc_avs_file = project_dir / "_scene_analysis.avs"
        sc_log_file = project_dir / "_scene_analysis.log"
        if sc_log_file.exists():
            sc_log_file.unlink()
        sc_avs_file.write_text(
            build_scenes_script(input_line, sc_log_file, args.scene_threshold),
            encoding="utf-8",
        )
        temp_files.extend([sc_avs_file, sc_log_file])

        run_avs(runner_cmd, sc_avs_file, cwd=project_dir,
                log_path=sc_log_file, label="scenes")
        if not sc_log_file.exists():
            raise RuntimeError("No log produced for scene analysis.")

        sc_flags, sc_diffs = parse_scenes_log(sc_log_file)
        if not sc_flags:
            print("No scene-analysis frames returned; aborting.",
                  file=sys.stderr)
            return 2
        last_frame = max(sc_flags)
        # Frame 0 is always flagged and is never a split.
        msc_scenes = {f for f, flag in sc_flags.items()
                      if flag == 1 and f > 0}
        spikes = (set(find_spikes(sc_diffs, args.spike_ratio))
                  if args.spike_ratio > 0 else set())
        scenes = sorted(msc_scenes | spikes)

        breaks_path = args.breaks or (project_dir / "Breaks.txt")
        breaks = load_breaks(breaks_path)

        # ---- Phase 3: Build workbook ----
        wb = Workbook()
        ws1 = wb.active
        ws1.title = SHEET1_NAME
        populate_frame_analysis(ws1, pd_results)

        ws2 = wb.create_sheet(SHEET2_NAME)
        populate_scene_ranges(ws2, scenes, breaks, last_frame)

        xlsx_path.parent.mkdir(parents=True, exist_ok=True)
        wb.save(xlsx_path)

        # ---- Summary ----
        print()
        for pd_name in PD_PARAMS:
            print(f"  {pd_name}: {len(pd_results[pd_name])} frames")
        print(f"  scene changes: {len(scenes)} "
              f"({len(msc_scenes)} from MSCDetection, score threshold > "
              f"{args.scene_threshold}; {len(spikes - msc_scenes)} more from "
              f"luma-difference spikes >= {args.spike_ratio}x)")
        if breaks_path.exists():
            print(f"  breaks loaded: {len(breaks)} from {breaks_path.name}")
        else:
            print(f"  breaks file not found at {breaks_path} (skipped)")
        print(f"  last frame (0-based): {last_frame}")
        print(f"  saved: {xlsx_path}")
    finally:
        if not args.keep_temp:
            for f in temp_files:
                try:
                    f.unlink()
                except FileNotFoundError:
                    pass

    finish("Make any corrections to frame_analysis.xlsx before moving on "
           "to Step 3.")
    return 0


if __name__ == "__main__":
    sys.exit(run_main())
