#!/usr/bin/env python3
"""
Step3.py  (build_mappings.py + analyze_combed.py in one pass)

Run after Step2.py and after any hand corrections to the "Scene Ranges"
sheet. Performs two phases against frame_analysis.xlsx:

Phase 1 -- Pulldown mappings (formerly build_mappings.py)
---------------------------------------------------------
For every row in "Scene Ranges" with start frame A in column A and end
frame B in column B:

    Column C = SUM of Sheet 1 column B (PD1) over frames A..B  (clean count)
    Column D = SUM of Sheet 1 column C (PD2) over frames A..B
    Column E = SUM of Sheet 1 column D (PD3) over frames A..B
    Column F = SUM of Sheet 1 column E (PD4) over frames A..B
    Column G = SUM of Sheet 1 column F (PD5) over frames A..B
    Column H = name of the winning pulldown (PD1..PD5)

Tiebreaker rules for column H when two or more of C..G tie at the max:
    C == D -> PD1
    D == E -> PD2
    E == F -> PD3
    F == G -> PD4
    G == C -> PD5

Rules are applied in the order listed above; the first one whose pair is
present in the set of tied-max columns wins. Non-adjacent or 3+ way ties
that no rule covers fall back to the leftmost tied column.

Each row's range is written to its winning mapping text file
(PD1Map.txt..PD5Map.txt) on its own line as "[A B]". The workbook is
saved at the end of this phase, before any AVS pass runs, because
S##E## IVTC.avs reads these mapping files in phase 2.

Phase 2 -- Orphan-field combing (formerly analyze_combed.py)
------------------------------------------------------------
Detects orphan-field residual combing by running two AviSynth passes and
correlating their results. Output goes to a third sheet
("Combed Frames") in frame_analysis.xlsx, and a flat DIMap.txt file.

Sheet 3 column layout (no header row; data starts at row 1):
    A : combed IVTC frame number (set by matching phase)
    B : DI-pass frame number
    C : change flag (0/1; 1 == an edit detected by MSCDetection)
    D : YDifferenceFromPrevious value, set only on edit rows + their
        previous row during edit-processing

Both passes are generated internally. Before phase 1 runs, each pass
script is opened for a single frame, so a broken source (a missing file
or plugin) fails in seconds instead of after the long DI pass.

Pass 1 (Scenes.avs `input = ...` source + QTGMC(preset="draft"))
    Per output frame, log: frame_index, YDifferenceFromPrevious,
    change_flag where change_flag = 1 when AverageLuma(MSCDetection_clip)
    > threshold (mirrors Scenes.avs's detection criterion).

Pass 2 (AVISource("S##E## IVTC.avs"); S##E## is taken from the folder
        path, as in Step1.py)
    Per output frame, log: frame_index, IsCombedTIVTC(2).

For each row N where change == 1:
    D[N]   = YDifferenceFromPrevious of frame N+1 (i.e. ydiff at N+1)
    D[N-1] = YDifferenceFromPrevious of frame N-1 (i.e. ydiff at N-1)
    The row of {N-1, N} with the higher D wins (ties go to N).
    The losing row is deleted, plus the 5 rows before and 5 rows after
    the winner -- 10 unique rows in total per edit.

For each combed frame K from pass 2, the surviving row whose column B
is closest to K * 2.5 receives K in its column A. Matching considers
ALL surviving rows from edit-processing (winners and non-edit, non-
deletion-zone rows alike).

Finally:
    1. Rows without a column-A value are deleted.
    2. Rows without a column-D value are deleted.

Surviving rows are written to sheet "Combed Frames", and each row's
"A B" pair (space-separated, no brackets) is written to DIMap.txt.
"""

import argparse
import bisect
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

from openpyxl import load_workbook


# --- Sheet names -----------------------------------------------------------

SHEET1_NAME = "Frame Analysis"
SHEET2_NAME = "Scene Ranges"
SHEET3_NAME = "Combed Frames"

# --- Mapping constants -----------------------------------------------------

PD_NAMES = ("PD1", "PD2", "PD3", "PD4", "PD5")
COL_TO_PD = {"C": "PD1", "D": "PD2", "E": "PD3", "F": "PD4", "G": "PD5"}

# --- Combed-analysis constants ---------------------------------------------

DI_THRESHOLD_DEFAULT = 30  # AverageLuma(sc) > N for MSCDetection-based change

EPISODE_RE = re.compile(r"S\d{2}E\d{2}", re.IGNORECASE)


# --------------------------------------------------------------------------
# Shared utilities
# --------------------------------------------------------------------------

def col_idx(letter: str) -> int:
    return ord(letter.upper()) - ord("A") + 1


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


def find_episode(project_dir: Path) -> str | None:
    """S##E## from the nearest folder in the path that has one, so a
    subfolder of an episode folder (e.g. "S03E01 The Search Part 1\\LD")
    works too."""
    for part in reversed(project_dir.parts):
        m = EPISODE_RE.search(part)
        if m:
            return m.group(0).upper()
    return None


def probe_avs(runner_template: list[str], script_text: str, probe_path: Path,
              cwd: Path) -> str | None:
    """Run `script_text` limited to its first frame. Returns the runner's
    error output on failure, or None when the script opens and renders."""
    probe_path.write_text(script_text + "Trim(0, -1)\n", encoding="utf-8")
    avs_str = str(probe_path)
    if any("{AVS}" in tok for tok in runner_template):
        cmd = [tok.replace("{AVS}", avs_str) for tok in runner_template]
    else:
        cmd = runner_template + [avs_str]
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if proc.returncode == 0:
        return None
    return proc.stderr.strip() or f"runner exited with code {proc.returncode}"


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
# Phase 1: Pulldown mappings
# --------------------------------------------------------------------------

def build_frame_lookup(ws1) -> dict[int, tuple[int, int, int, int, int]]:
    """Return {frame_number: (PD1, PD2, PD3, PD4, PD5)} from Sheet 1.

    Sheet 1 layout: row 1 = headers, row 2.. = data
        col A = Frame, col B..F = PD1..PD5 (0=combed, 1=clean)
    Missing cells are treated as 0.
    """
    lookup: dict[int, tuple[int, int, int, int, int]] = {}
    for row in ws1.iter_rows(min_row=2, values_only=True):
        if not row or row[0] is None:
            continue
        try:
            frame = int(row[0])
        except (TypeError, ValueError):
            continue
        vals = []
        for i in range(1, 6):
            v = row[i] if i < len(row) else None
            try:
                vals.append(int(v) if v is not None else 0)
            except (TypeError, ValueError):
                vals.append(0)
        lookup[frame] = tuple(vals)  # type: ignore[assignment]
    return lookup


def pick_winner(c: int, d: int, e: int, f: int, g: int) -> str:
    """Choose PD1..PD5 by max value with the documented tiebreaker rules."""
    vals = {"C": c, "D": d, "E": e, "F": f, "G": g}
    mx = max(vals.values())
    tied = {k for k, v in vals.items() if v == mx}

    if len(tied) == 1:
        return COL_TO_PD[next(iter(tied))]

    rules = (
        ({"C", "D"}, "PD1"),
        ({"D", "E"}, "PD2"),
        ({"E", "F"}, "PD3"),
        ({"F", "G"}, "PD4"),
        ({"G", "C"}, "PD5"),
    )
    for pair, pd_name in rules:
        if pair.issubset(tied):
            return pd_name

    # No adjacent-pair rule matched (e.g. {C, E}); fall back to leftmost.
    leftmost = min(tied)  # lexicographic min among C..G == leftmost column
    return COL_TO_PD[leftmost]


def build_mappings(ws1, ws2, project_dir: Path) -> dict[str, int]:
    """Fill Scene Ranges columns C..H and write PD1Map.txt..PD5Map.txt.
    Returns the number of ranges written to each mapping file."""
    frames = build_frame_lookup(ws1)
    if not frames:
        raise RuntimeError(f"No frame data found in sheet {SHEET1_NAME!r}")

    mapping_paths = {pd: project_dir / f"{pd}Map.txt" for pd in PD_NAMES}
    mapping_files = {pd: p.open("w", encoding="utf-8")
                     for pd, p in mapping_paths.items()}
    row_counts = {pd: 0 for pd in PD_NAMES}

    try:
        for row_idx in range(1, ws2.max_row + 1):
            a_val = ws2.cell(row=row_idx, column=1).value
            b_val = ws2.cell(row=row_idx, column=2).value
            if a_val is None or b_val is None:
                continue
            try:
                a = int(a_val)
                b = int(b_val)
            except (TypeError, ValueError):
                continue
            if b < a:
                continue

            # Sum each PD column across the range A..B (inclusive)
            sums = [0, 0, 0, 0, 0]
            for f in range(a, b + 1):
                entry = frames.get(f)
                if entry is None:
                    continue
                for i in range(5):
                    sums[i] += entry[i]

            pd1, pd2, pd3, pd4, pd5 = sums
            ws2.cell(row=row_idx, column=col_idx("C"), value=pd1)
            ws2.cell(row=row_idx, column=col_idx("D"), value=pd2)
            ws2.cell(row=row_idx, column=col_idx("E"), value=pd3)
            ws2.cell(row=row_idx, column=col_idx("F"), value=pd4)
            ws2.cell(row=row_idx, column=col_idx("G"), value=pd5)

            winner = pick_winner(pd1, pd2, pd3, pd4, pd5)
            ws2.cell(row=row_idx, column=col_idx("H"), value=winner)

            mapping_files[winner].write(f"[{a} {b}]\n")
            row_counts[winner] += 1
    finally:
        for fh in mapping_files.values():
            fh.close()

    return row_counts


# --------------------------------------------------------------------------
# Phase 2: Orphan-field combing
# --------------------------------------------------------------------------

def build_di_script(input_line: str, log_path: Path, threshold: int) -> str:
    """QTGMC + MVTools MSCDetection (for change detection) plus
    YDifferenceFromPrevious (for the column-D comparison values).

    Logs (frame, ydiff, change) per frame, where:
        ydiff  = YDifferenceFromPrevious() (0.0 for frame 0)
        change = 1 when AverageLuma(MSCDetection_clip) > threshold
    """
    log_str = str(log_path).replace("\\", "/")
    return (
        f"{input_line}\n"
        f'clip = input.QTGMC(preset="draft")\n'
        f"clip\n"
        f"global super = last.MSuper(pel=2, sharp=2)\n"
        f"global vec = MAnalyse(super, isb=false, blksize=16, delta=1)\n"
        f"global sc = MSCDetection(last, vec, thSCD1=400, thSCD2=130)\n"
        f'clip2 = ScriptClip(last, """\n'
        f"    global cur_score = AverageLuma(sc)\n"
        f"    global cur_ydiff = current_frame > 0 ? YDifferenceFromPrevious() : 0.0\n"
        f'""")\n'
        f'WriteFile(clip2, "{log_str}", '
        f'"current_frame", """ "," """, '
        f'"cur_ydiff", """ "," """, '
        f'"cur_score > {threshold} ? 1 : 0", '
        f'append=false, flush=true)\n'
    )


def build_ivtc_script(input_line: str, log_path: Path) -> str:
    """Per-frame log of (frame, IsCombedTIVTC) for the S##E## IVTC.avs source."""
    log_str = str(log_path).replace("\\", "/")
    return (
        f"{input_line}\n"
        f'WriteFile(input, "{log_str}", '
        f'"current_frame", """ "," """, '
        f'"IsCombedTIVTC(2) ? 1 : 0", '
        f'append=false, flush=true)\n'
    )


def parse_di_log(log_path: Path) -> list[dict]:
    """Parse 'frame,ydiff,change' lines into a list of row dicts."""
    rows: list[dict] = []
    with log_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) != 3:
                continue
            try:
                frame = int(parts[0])
                ydiff = float(parts[1])
                change = int(parts[2])
            except ValueError:
                continue
            rows.append({
                "frame": frame, "ydiff": ydiff, "change": change,
                "d": None, "a": None,
            })
    rows.sort(key=lambda r: r["frame"])
    return rows


def parse_ivtc_log(log_path: Path) -> list[int]:
    combed: list[int] = []
    with log_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) != 2:
                continue
            try:
                frame = int(parts[0])
                flag = int(parts[1])
            except ValueError:
                continue
            if flag == 1:
                combed.append(frame)
    return combed


def process_edits(rows: list[dict]) -> list[dict]:
    """For each row N where change==1:
        D[N]   = ydiff at frame N+1
        D[N-1] = ydiff at frame N-1
    Compare D[N] and D[N-1]; the higher wins (ties go to row N).
    Mark for deletion: loser + 5 rows before and 5 rows after the winner
    (10 unique rows when the loser overlaps with the surrounding zone).

    All deletions are unioned across edits, then applied in one pass.
    Returns the surviving rows.
    """
    n = len(rows)
    deleted: set[int] = set()
    for i in range(n):
        if rows[i]["change"] != 1:
            continue
        if i - 1 < 0 or i + 1 >= n:
            continue  # need both neighbors for D values

        d_at_N = rows[i + 1]["ydiff"]      # YDiffPrev at frame N+1
        d_at_Nm1 = rows[i - 1]["ydiff"]    # YDiffPrev at frame N-1
        rows[i]["d"] = d_at_N
        rows[i - 1]["d"] = d_at_Nm1

        if d_at_N >= d_at_Nm1:
            winner = i
            loser = i - 1
        else:
            winner = i - 1
            loser = i

        deleted.add(loser)
        for offset in (-5, -4, -3, -2, -1, 1, 2, 3, 4, 5):
            k = winner + offset
            if 0 <= k < n:
                deleted.add(k)

    return [r for idx, r in enumerate(rows) if idx not in deleted]


def assign_combed_to_rows(rows: list[dict], combed_frames: list[int]) -> None:
    """For each combed IVTC frame K, find the row whose column B is
    closest to K * 2.5 and write K into that row's column A.

    Considers ALL provided rows as match candidates (per the literal
    spec: matching is over all surviving rows from edit-processing,
    not only winners). Non-winner matches will be culled later by the
    final 'delete without D' filter."""
    if not rows:
        return
    rows_sorted = sorted(rows, key=lambda r: r["frame"])
    b_values = [r["frame"] for r in rows_sorted]
    for k in combed_frames:
        target = k * 2.5
        idx = bisect.bisect_left(b_values, target)
        cands = []
        if idx > 0:
            cands.append(idx - 1)
        if idx < len(b_values):
            cands.append(idx)
        if not cands:
            continue
        best = min(cands, key=lambda i: abs(b_values[i] - target))
        rows_sorted[best]["a"] = k


def populate_combed_frames(wb, rows: list[dict]) -> None:
    """Write final filtered rows to Sheet 3 using columns A-D only.
        A = combed IVTC frame, B = frame, C = change flag, D = ydiff
    No header row; data starts at row 1.
    """
    if SHEET3_NAME in wb.sheetnames:
        del wb[SHEET3_NAME]
    ws = wb.create_sheet(SHEET3_NAME)

    for i, r in enumerate(rows, start=1):
        ws.cell(row=i, column=1, value=r["a"])
        ws.cell(row=i, column=2, value=r["frame"])
        ws.cell(row=i, column=3, value=r["change"])
        ws.cell(row=i, column=4, value=r["d"])


def write_dimap(dimap_path: Path, rows: list[dict]) -> None:
    with dimap_path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(f"{r['a']} {r['frame']}\n")


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
                        help="Folder with Scenes.avs / S##E## IVTC.avs and "
                             "for the output text files (default: script dir)")
    parser.add_argument("--xlsx", type=Path, default=None,
                        help="Workbook to read/update "
                             "(default: <project>/frame_analysis.xlsx)")
    parser.add_argument("--runner", type=parse_runner, default=None,
                        help='AVS runner command with {AVS} placeholder, e.g. '
                             '"ffmpeg -hide_banner -loglevel error -y -i {AVS} '
                             '-f null -"')
    parser.add_argument("--threshold", type=int, default=DI_THRESHOLD_DEFAULT,
                        help=f"AverageLuma(sc) change threshold for DI pass "
                             f"(default: {DI_THRESHOLD_DEFAULT})")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep the generated AVS and log files for inspection")
    args = parser.parse_args()

    project_dir: Path = args.project_dir.resolve()
    xlsx_path: Path = (args.xlsx or project_dir / "frame_analysis.xlsx").resolve()
    runner_cmd = args.runner or default_runner()

    # Check everything both phases need before touching any output.
    if not xlsx_path.exists():
        print(f"Workbook not found: {xlsx_path}", file=sys.stderr)
        return 1
    scenes_avs = project_dir / "Scenes.avs"
    if not scenes_avs.exists():
        print(f"Missing required AVS: {scenes_avs} (run Step1.py first)",
              file=sys.stderr)
        return 1
    episode = find_episode(project_dir)
    if episode is None:
        print(f"No episode number (S##E##) found in folder path: "
              f"{project_dir}", file=sys.stderr)
        return 1
    ivtc_avs = project_dir / f"{episode} IVTC.avs"
    if not ivtc_avs.exists():
        print(f"Missing required AVS: {ivtc_avs} (run Step1.py first)",
              file=sys.stderr)
        return 1

    wb = load_workbook(xlsx_path)
    for needed in (SHEET1_NAME, SHEET2_NAME):
        if needed not in wb.sheetnames:
            print(f"Missing sheet {needed!r} in {xlsx_path}", file=sys.stderr)
            return 2

    di_input = extract_input_line(scenes_avs)
    ivtc_input = f'input = AVISource("{ivtc_avs.name}")'

    di_avs_file = project_dir / "_di_analyze.avs"
    di_log = project_dir / "_di_analyze.log"
    ivtc_avs_file = project_dir / "_ivtc_comb.avs"
    ivtc_log = project_dir / "_ivtc_comb.log"
    probe_file = project_dir / "_probe.avs"
    temp_files = [di_avs_file, di_log, ivtc_avs_file, ivtc_log, probe_file]

    di_script = build_di_script(di_input, di_log, args.threshold)
    ivtc_script = build_ivtc_script(ivtc_input, ivtc_log)

    try:
        # ---- Preflight: open each pass script for one frame ----
        for label, script, source in (("DI", di_script, scenes_avs.name),
                                      ("IVTC", ivtc_script, ivtc_avs.name)):
            print(f"[{label}] checking that {source} opens...")
            err = probe_avs(runner_cmd, script, probe_file, project_dir)
            if err is not None:
                print(f"\n{label} pass cannot run; nothing was changed.\n"
                      f"Fix {source} (or a file it loads) and run Step3.py "
                      f"again.\n\n{err}", file=sys.stderr)
                return 5
        for lf in (di_log, ivtc_log):
            if lf.exists():
                lf.unlink()
        print()

        # ---- Phase 1: Pulldown mappings ----
        try:
            row_counts = build_mappings(wb[SHEET1_NAME], wb[SHEET2_NAME],
                                        project_dir)
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return 3
        wb.save(xlsx_path)

        print(f"Updated {xlsx_path}  (sheet: {SHEET2_NAME!r})")
        for pd in PD_NAMES:
            print(f"  {pd}Map.txt: {row_counts[pd]} range(s)")
        print()

        # ---- Phase 2: Orphan-field combing ----
        di_avs_file.write_text(di_script, encoding="utf-8")
        ivtc_avs_file.write_text(ivtc_script, encoding="utf-8")

        # Pass 1
        run_avs(runner_cmd, di_avs_file, project_dir, di_log, "DI")
        # Pass 2
        run_avs(runner_cmd, ivtc_avs_file, project_dir, ivtc_log, "IVTC")

        rows = parse_di_log(di_log)
        if not rows:
            print("No DI frames analyzed; aborting.", file=sys.stderr)
            return 4

        n_changes = sum(1 for r in rows if r["change"] == 1)
        survivors = process_edits(rows)
        n_with_d = sum(1 for r in survivors if r["d"] is not None)
        print(f"DI rows: {len(rows)}  change frames: {n_changes}  "
              f"survivors after edit-processing: {len(survivors)} "
              f"(of which {n_with_d} have a D value)")

        combed = parse_ivtc_log(ivtc_log)
        print(f"IVTC combed frames: {len(combed)}")

        assign_combed_to_rows(survivors, combed)

        # Final filters: drop rows without A, then drop rows without D.
        with_a = [r for r in survivors if r["a"] is not None]
        final = [r for r in with_a if r["d"] is not None]
        final.sort(key=lambda r: r["a"])
        print(f"Combed-assigned rows: {len(with_a)}  "
              f"surviving 'no D' filter: {len(final)}")

        populate_combed_frames(wb, final)
        wb.save(xlsx_path)
        dimap_path = project_dir / "DIMap.txt"
        write_dimap(dimap_path, final)

        print(f"Saved: {xlsx_path}  (sheet: {SHEET3_NAME!r})")
        print(f"Saved: {dimap_path}")
    finally:
        if not args.keep_temp:
            for f in temp_files:
                try:
                    f.unlink()
                except FileNotFoundError:
                    pass

    finish("You can now finish fixing up the episode.")
    return 0


if __name__ == "__main__":
    sys.exit(run_main())
