import os
import re
from datetime import datetime, timedelta

# === Set the working directory ===
directory = "/home/liu/gps-sdr-sim"

# === Prompt for the navigation file name ===
def get_manual_filename():
    day_of_year = input("Enter the day of year (001-365):").zfill(3)
    year = input("Enter the two-digit year (e.g. 24):").zfill(2)
    return f"brdc{day_of_year}0.{year}n"

# === Derived file name ===
def get_processed_filename(original_filename):
    name, ext = os.path.splitext(original_filename)
    return f"{name}{ext}"

# === Format TOC (line 1) ===
def format_toc_line(line, hour_offset=2):
    prefix = line[:3]
    time_field = line[3:22]
    rest = line[22:]
    try:
        dt = datetime.strptime(time_field.replace('  ', ' 0'), "%y %m %d %H %M %S.%f")
    except ValueError:
        dt = datetime.strptime(time_field.replace('  ', ' 0'), "%y %m %d %H %M %S")
    dt += timedelta(hours=hour_offset)
    toc_str = (
        f"{dt.year % 100:2d}{dt.month:3d}{dt.day:3d}"
        f"{dt.hour:3d}{dt.minute:3d} {dt.second:4.1f}"
    )
    return prefix + toc_str + rest

# === Format as 0.XXXXD±YY and shift exponent +1 ===
def format_toe_special(f):
    f += 7200
    sign = "-" if f < 0 else " "
    mantissa, exp = f"{abs(f):.12E}".split("E")
    new_exp = int(exp) + 1
    formatted = f"{sign}0.{mantissa[2:]}D{new_exp:+03d}"
    # Remove one leading space and pad at the end to length 19
    return formatted.strip().ljust(19)

# === Format transmission time using 19 characters ===
def format_19(f):
    return f"{f: 19.12E}".replace("E", "D")

# === Adjust block: modify TOC, TOE and transmission time ===
def adjust_time_values(block, hour_offset=2):
    new_block = block.copy()

    # === TOC first line ===
    new_block[0] = format_toc_line(new_block[0], hour_offset)

    # === TOE (line 4, column 1) ===
    try:
        toe_line = new_block[3]
        toe_field = toe_line[4:23]
        toe_val = float(toe_field.replace("D", "E"))
        new_toe = format_toe_special(toe_val)
        new_block[3] = toe_line[:4] + new_toe + toe_line[23:]
    except:
        pass

    # === Transmission time (line 7) ===
    try:
        line = new_block[6]
        matches = list(re.finditer(r"[ \-]?\d+\.\d+D[+\-]\d+", line))
        for match in reversed(matches):
            val = float(match.group(0).replace("D", "E"))
            if 0 <= val <= 604800:
                val += 7200
                new_val = format_19(val)
                start, end = match.span()
                new_block[6] = line[:start] + new_val + line[end:]
                break
    except:
        pass

    return new_block

# === Main processing flow ===
def process_ephemeris(file_path, processed_file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find the last hour
    last_hour = None
    for i in range(len(lines)-1, -1, -1):
        line = lines[i]
        if len(line) >= 19 and line[0].isdigit():
            time_str = line[3:19].replace("  ", " 0")
            last_time = datetime.strptime(time_str, "%y %m %d %H %M %S")
            last_hour = last_time.hour
            break

    # Find the block for hour -1
    blocks = []
    if last_hour is not None:
        target_hour = last_hour - 1
        for i in range(len(lines)-1, -1, -1):
            line = lines[i]
            if len(line) >= 19 and line[0].isdigit():
                time_str = line[3:19].replace("  ", " 0")
                record_time = datetime.strptime(time_str, "%y %m %d %H %M %S")
                if record_time.hour == target_hour:
                    block = lines[i:i+8]
                    blocks.insert(0, block)
                elif record_time.hour < target_hour:
                    break

    # Output file
    with open(processed_file_path, 'w') as f:
        f.writelines(lines)
        if blocks:
            print(f"🔵 Found {len(blocks)} block(s) to extend by +2 hours")
            for block in blocks:
                new_block = adjust_time_values(block)
                for line in new_block:
                    f.write(line if line.endswith("\n") else line + "\n")
                print(f"✅ Written: {new_block[0].strip()}")

    print(f"✅ Extension processing completed → {processed_file_path}")

# === Main entry point ===
if __name__ == "__main__":
    file_name = get_manual_filename()
    file_path = os.path.join(directory, file_name)
    processed_file_name = get_processed_filename(file_name)
    processed_file_path = os.path.join(directory, processed_file_name)

    if not os.path.isfile(file_path):
        print(f"❌ File not found {file_path}")
    else:
        process_ephemeris(file_path, processed_file_path)
