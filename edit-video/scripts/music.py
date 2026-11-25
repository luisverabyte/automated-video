#!/usr/bin/env python3
"""Adds background music that ducks on its own when you talk and fades out at the end.

  python3 music.py video.mp4 song.mp3 -o with-music.mp4 [--volume -20]

--volume is how many dB the music sits below your voice when you're not talking (default -20; more negative = quieter).
Use royalty-free music cleared for social media (for example, the YouTube Audio Library, Mixkit or Pixabay Music).
Requirements: ffmpeg and ffprobe on the PATH.
"""
import argparse
import shutil
import subprocess
import sys


def main():
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is missing. Install it: https://ffmpeg.org/download.html")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("music")
    ap.add_argument("-o", "--output", default="with-music.mp4")
    ap.add_argument("--volume", type=float, default=-20)
    a = ap.parse_args()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                a.video], check=True, capture_output=True, text=True).stdout.strip())
    graph = (f"[1:a]volume={a.volume}dB,afade=t=in:d=0.5,afade=t=out:st={max(0, dur - 1.5):.2f}:d=1.5[m];"
             "[0:a]asplit=2[voice][key];"
             "[m][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];"
             "[voice][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", a.video, "-stream_loop", "-1", "-i", a.music,
                    "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-t", f"{dur:.3f}", "-movflags", "+faststart", a.output], check=True)
    print(f"done: {a.output}")


if __name__ == "__main__":
    main()
