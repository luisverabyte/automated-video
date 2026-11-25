#!/usr/bin/env python3
"""Cuts silences and bad takes, alternates a slight zoom between cuts and sets the video to vertical 1080x1920.

  python3 cut.py raw.mp4 -o cut.mp4                     # detects the silences on its own
  python3 cut.py raw.mp4 -o cut.mp4 --list              # only lists the segments, doesn't cut
  python3 cut.py raw.mp4 -o cut.mp4 --segments s.txt    # uses your segments: one "start end" line in seconds

By default it removes pauses of 0.6 s or more, leaves 0.15 s of breathing room on each side of the voice and
alternates the framing between 100% and 110% on each cut (the jump feels like a camera change, not a mistake).

Requirements: ffmpeg and ffprobe on the PATH. No Python dependencies.
"""
import argparse
import re
import shutil
import subprocess
import sys


def duration(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def silences(video, threshold_db, pause):
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", video, "-vn", "-af",
                          f"silencedetect=noise={threshold_db}dB:d={pause}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def voice_segments(video, threshold_db, pause, margin, minimum):
    total = duration(video)
    segments, cursor = [], 0.0
    for s_start, s_end in silences(video, threshold_db, pause):
        if s_start - cursor > 0:
            segments.append([cursor, s_start])
        cursor = s_end if s_end is not None else total
    if total - cursor > 0:
        segments.append([cursor, total])
    padded = []
    for a, b in segments:
        a, b = max(0.0, a - margin), min(total, b + margin)
        if padded and a <= padded[-1][1]:
            padded[-1][1] = b
        else:
            padded.append([a, b])
    return [s for s in padded if s[1] - s[0] >= minimum]


def read_segments(path):
    segments = []
    for line in open(path, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if line:
            a, b = line.split()[:2]
            segments.append([float(a), float(b)])
    return segments


def main():
    for b in ("ffmpeg", "ffprobe"):
        if not shutil.which(b):
            sys.exit("ffmpeg is missing. Install it: https://ffmpeg.org/download.html")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--output", default="cut.mp4")
    ap.add_argument("--segments", help="file with 'start end' per line; otherwise silences are detected")
    ap.add_argument("--pause", type=float, default=0.6, help="shortest silence that gets removed (s)")
    ap.add_argument("--threshold", type=float, default=-35, help="dB below which audio counts as silence")
    ap.add_argument("--margin", type=float, default=0.15, help="breathing room left on each side of the voice (s)")
    ap.add_argument("--minimum", type=float, default=0.3, help="shorter segments are dropped (s)")
    ap.add_argument("--zoom", type=float, default=1.10, help="zoom on alternate cuts; 1 = no zoom")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--list", action="store_true", help="only list the segments")
    a = ap.parse_args()

    segments = read_segments(a.segments) if a.segments else voice_segments(a.video, a.threshold, a.pause, a.margin, a.minimum)
    if not segments:
        sys.exit("No voice found. Try --threshold -45.")
    total = sum(b - a_ for a_, b in segments)
    print(f"{len(segments)} segments, {total:.1f} s of {duration(a.video):.1f} s")
    for i, (x, y) in enumerate(segments):
        print(f"{x:8.2f} {y:8.2f}   # segment {i + 1}")
    if a.list:
        return

    W, H = a.width, a.height
    # Fills the vertical frame without distortion (crops the excess) and applies the alternating zoom.
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    parts, concat = [], ""
    for i, (x, y) in enumerate(segments):
        z = a.zoom if i % 2 else 1.0
        zoom = "" if z == 1.0 else f",scale=iw*{z}:ih*{z},crop={W}:{H}"
        parts.append(f"[0:v]trim={x}:{y},setpts=PTS-STARTPTS,{base}{zoom}[v{i}];"
                     f"[0:a]atrim={x}:{y},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                     f"afade=t=out:st={max(0, y - x - 0.01):.3f}:d=0.01[a{i}];")
        concat += f"[v{i}][a{i}]"
    graph = "".join(parts) + f"{concat}concat=n={len(segments)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", a.video, "-filter_complex", graph,
                    "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.output],
                   check=True)
    print(f"done: {a.output}")


if __name__ == "__main__":
    main()
