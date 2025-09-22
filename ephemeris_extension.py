"""Ephemeris extension helper for GPS spoofing experiments."""

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clone the latest navigation block and extend TOC/TOE by a time offset.",
    )
    parser.add_argument(
        "--rinex",
        type=Path,
        help="Path to the input RINEX navigation file (e.g. brdc1760.24n).",
    )
    parser.add_argument(
        "--offset-hours",
        type=float,
        default=2.0,
        help="Hours to extend the navigation block by (default: 2).",
    )
    parser.add_argument(
        "--workdir",
        type=Path,
        help="Directory for the output file (defaults to the input file directory).",
    )
    parser.add_argument(
        "--suffix",
        default="_eem",
        help="Suffix appended before the file extension (default: _eem).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Explicit output path (overrides --workdir and --suffix).",
    )
    parser.add_argument(
        "--prompt",
        action="store_true",
        help="Prompt for a day-of-year filename when --rinex is not supplied.",
    )
    return parser.parse_args()


def prompt_for_rinex() -> Path:
    day_of_year = input("Enter the day of year (001-366):").strip().zfill(3)
    year = input("Enter the two-digit year (e.g. 24):").strip().zfill(2)
    return Path(f"brdc{day_of_year}0.{year}n")


def derive_output_path(
    input_path: Path, workdir: Optional[Path], suffix: str, explicit: Optional[Path]
) -> Path:
    if explicit is not None:
        return explicit

    directory = workdir if workdir is not None else input_path.parent
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{input_path.stem}{suffix}{input_path.suffix}"


def format_toc_line(line: str, offset_seconds: float) -> str:
    prefix = line[:3]
    time_field = line[3:22]
    rest = line[22:]
    try:
        dt = datetime.strptime(time_field.replace("  ", " 0"), "%y %m %d %H %M %S.%f")
    except ValueError:
        dt = datetime.strptime(time_field.replace("  ", " 0"), "%y %m %d %H %M %S")
    dt += timedelta(seconds=offset_seconds)
    toc_str = (
        f"{dt.year % 100:2d}{dt.month:3d}{dt.day:3d}"
        f"{dt.hour:3d}{dt.minute:3d} {dt.second:4.1f}"
    )
    return prefix + toc_str + rest


def format_toe_value(value: float, offset_seconds: float) -> str:
    value += offset_seconds
    sign = "-" if value < 0 else " "
    mantissa, exponent = f"{abs(value):.12E}".split("E")
    new_exp = int(exponent) + 1
    formatted = f"{sign}0.{mantissa[2:]}D{new_exp:+03d}"
    return formatted.strip().ljust(19)


def format_transmission_time(value: float, offset_seconds: float) -> str:
    value += offset_seconds
    return f"{value: 19.12E}".replace("E", "D")


def adjust_time_values(block: List[str], offset_seconds: float) -> List[str]:
    new_block = block.copy()
    new_block[0] = format_toc_line(new_block[0], offset_seconds)

    try:
        toe_line = new_block[3]
        toe_field = toe_line[4:23]
        toe_val = float(toe_field.replace("D", "E"))
        new_toe = format_toe_value(toe_val, offset_seconds)
        new_block[3] = toe_line[:4] + new_toe + toe_line[23:]
    except Exception:
        pass

    try:
        line = new_block[6]
        matches = list(re.finditer(r"[ \-]?\d+\.\d+D[+\-]\d+", line))
        for match in reversed(matches):
            val = float(match.group(0).replace("D", "E"))
            if 0 <= val <= 604800:
                new_val = format_transmission_time(val, offset_seconds)
                start, end = match.span()
                new_block[6] = line[:start] + new_val + line[end:]
                break
    except Exception:
        pass

    return new_block


def find_blocks(lines: List[str]) -> List[List[str]]:
    last_hour = None
    for idx in range(len(lines) - 1, -1, -1):
        line = lines[idx]
        if len(line) >= 19 and line[0].isdigit():
            time_str = line[3:19].replace("  ", " 0")
            last_time = datetime.strptime(time_str, "%y %m %d %H %M %S")
            last_hour = last_time.hour
            break

    if last_hour is None:
        return []

    target_hour = last_hour - 1
    blocks: List[List[str]] = []
    for idx in range(len(lines) - 1, -1, -1):
        line = lines[idx]
        if len(line) >= 19 and line[0].isdigit():
            time_str = line[3:19].replace("  ", " 0")
            record_time = datetime.strptime(time_str, "%y %m %d %H %M %S")
            if record_time.hour == target_hour:
                block = lines[idx : idx + 8]
                blocks.insert(0, block)
            elif record_time.hour < target_hour:
                break

    return blocks


def process_ephemeris(input_path: Path, output_path: Path, offset_hours: float) -> None:
    offset_seconds = offset_hours * 3600.0
    lines = input_path.read_text().splitlines(keepends=True)
    blocks = find_blocks(lines)

    with output_path.open("w") as fh:
        fh.writelines(lines)
        if blocks:
            print(f"🔵 Found {len(blocks)} block(s) to extend by +{offset_hours} hour(s)")
            for block in blocks:
                new_block = adjust_time_values(block, offset_seconds)
                for entry in new_block:
                    fh.write(entry if entry.endswith("\n") else f"{entry}\n")
                print(f"✅ Written: {new_block[0].strip()}")
        else:
            print("⚪ No eligible blocks detected; output matches the original file.")

    print(f"✅ Extension processing completed → {output_path}")


def main() -> int:
    args = parse_args()

    input_path = args.rinex
    if input_path is None:
        if args.prompt:
            input_path = prompt_for_rinex()
        else:
            print("❌ Provide --rinex or use --prompt for interactive mode", file=sys.stderr)
            return 1

    input_path = input_path.expanduser().resolve()
    if not input_path.is_file():
        print(f"❌ File not found: {input_path}", file=sys.stderr)
        return 1

    if args.output and args.workdir:
        print("❌ Use either --output or --workdir (not both)", file=sys.stderr)
        return 1

    workdir = args.workdir.expanduser().resolve() if args.workdir else None
    output = args.output.expanduser().resolve() if args.output else None
    output_path = derive_output_path(input_path, workdir, args.suffix, output)

    process_ephemeris(input_path, output_path, args.offset_hours)
    return 0


if __name__ == "__main__":
    sys.exit(main())
