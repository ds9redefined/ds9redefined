#!/usr/bin/env python3
"""
list_combed.py

Runs a single AviSynth pass on IVTC-Comb.avs and writes the frame
numbers of every combed frame to combed.txt (one frame number per line).

The combing test is IsCombedTIVTC(N) where N defaults to 4. Override
with --threshold if needed.
"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path


COMBED_CTHRESH = 4


def extract_input_line(avs_path: Path) -> str:
    pattern = re.compile(r"^\s*input\s*=", re.IGNORECASE)
    with avs_path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            if pattern.match(raw):
                return raw.rstrip("\n")
    raise RuntimeError(f"Could not find 'input = ...' line in {avs_path}")


def build_script(input_line: str, log_path: Path, cthresh: int) -> str:
    """Per-frame log of (frame, IsCombedTIVTC) for the IVTC-Comb source."""
    log_str = str(log_path).replace("\\", "/")
    return (
        f"{input_line}\n"
        f'WriteFile(input, "{log_str}", '
        f'"current_frame", """ "," """, '
        f'"IsCombedTIVTC({cthresh}) ? 1 : 0", '
        f'append=false, flush=true)\n'
    )


def _count_lines(path: Path) -> int:
    try:
        with path.open("rb") as fh:
            return sum(1 for _ in fh)
    except FileNotFoundError:
        return 0


def run_avs(runner_template: list[str], avs_path: Path, cwd: Path,
            log_path: Path, label: str, poll_interval: float = 0.2) -> None:
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


def parse_log(log_path: Path) -> list[int]:
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


def default_runner() -> list[str]:
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", "{AVS}", "-f", "null", "-",
    ]


def parse_runner(value: str) -> list[str]:
    return value.split()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--project-dir", type=Path,
                        default=Path(__file__).resolve().parent,
                        help="Folder containing IVTC-Comb.avs "
                             "(default: script dir)")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output text file "
                             "(default: <project>/combed.txt)")
    parser.add_argument("--runner", type=parse_runner, default=None,
                        help='AVS runner command with {AVS} placeholder')
    parser.add_argument("--threshold", type=int, default=COMBED_CTHRESH,
                        help=f"IsCombedTIVTC cthresh "
                             f"(default: {COMBED_CTHRESH})")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep the generated AVS and log files")
    args = parser.parse_args()

    project_dir: Path = args.project_dir.resolve()
    avs_path = project_dir / "IVTC-Comb.avs"
    if not avs_path.exists():
        print(f"IVTC-Comb.avs not found at {avs_path}", file=sys.stderr)
        return 1

    output_path: Path = (args.output or project_dir / "combed.txt").resolve()
    runner_cmd = args.runner or default_runner()

    input_line = extract_input_line(avs_path)

    avs_file = project_dir / "_list_combed.avs"
    log_file = project_dir / "_list_combed.log"
    if log_file.exists():
        log_file.unlink()

    avs_file.write_text(
        build_script(input_line, log_file, args.threshold),
        encoding="utf-8",
    )

    temp_files = [avs_file, log_file]
    try:
        run_avs(runner_cmd, avs_file, project_dir, log_file, "IVTC")

        if not log_file.exists():
            raise RuntimeError(
                "No log produced; AVS likely processed no frames. "
                "Check the runner command."
            )

        combed = parse_log(log_file)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fh:
            for f in combed:
                fh.write(f"{f}\n")

        print(f"Combed frames: {len(combed)}")
        print(f"Saved: {output_path}")
    finally:
        if not args.keep_temp:
            for f in temp_files:
                try:
                    f.unlink()
                except FileNotFoundError:
                    pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
