#!/usr/bin/env python3
"""Word-by-word subtitles, free and on your own computer.

Two steps, so you can correct the transcript before burning it in:

  1) python3 subtitles.py transcribe video.mp4 -o transcript.json [--model small] [--language en] [--script script.md]
  2) python3 subtitles.py burn video.mp4 transcript.json -o final.mp4 [--ds design-system.md] [--fonts folder]

Step 1 uses faster-whisper (OpenAI's Whisper, runs locally at no cost).
Step 2 builds an .ass file with the style from your design-system.md (subtitles section), burns it in with ffmpeg
and also leaves an .srt next to it, in case the platform asks you to upload the subtitles separately.

Requirements: ffmpeg on the PATH, Python 3.9+, `pip install faster-whisper pyyaml numpy`.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

# Defaults of the design-system-v1 format (DESIGN-SYSTEM-FORMAT.md).
DEFAULTS = {
    "font": "",
    "weight": 800,
    "size_px": 64,
    "color": "#FFFFFF",
    "highlight": "primary",
    "outline": {"color": "#000000", "width_px": 6},
    "box": False,
    "position": "center",
    "words_per_line": 3,
    "lines": 1,
    "uppercase": False,
}
DEFAULT_ZONE = {"x": [120, 960], "y": [270, 1250]}
BASE_W, BASE_H = 1080, 1920
BREAK_PAUSE = 0.5  # seconds of silence that start a new subtitle block


def warn(msg):
    print(f"[subtitles] {msg}", file=sys.stderr)


# ---------- design-system.md ----------

def read_ds(path):
    if not path:
        return {}
    text = open(path, encoding="utf-8").read()
    m = re.search(r"```ya?ml\s*\n(.*?)```", text, re.S)
    if not m:
        warn(f"{path} has no ```yaml``` block; using defaults.")
        return {}
    try:
        import yaml
    except ImportError:
        warn("pyyaml is missing (pip install pyyaml); using defaults.")
        return {}
    data = yaml.safe_load(m.group(1)) or {}
    fmt = data.get("format", "")
    if fmt and fmt != "design-system-v1":
        warn(f"format {fmt} isn't design-system-v1; reading what I recognize.")
    if "subtitulos" in data and "subtitles" not in data:
        warn("this design-system.md uses the Spanish keys (video-automatico); use the Spanish edition's scripts or rebuild it with this kit.")
    return data


def style_from_ds(ds):
    sub = dict(DEFAULTS)
    sub.update({k: v for k, v in (ds.get("subtitles") or {}).items() if v not in (None, "")})
    missing = [k for k in DEFAULTS if k not in (ds.get("subtitles") or {})]
    if ds and missing:
        warn("subtitles without " + ", ".join(missing) + ": using defaults.")
    color = ds.get("color") or {}
    typo = ds.get("typography") or {}
    video = ds.get("video") or {}
    if not sub.get("font"):
        sub["font"] = (typo.get("headings") or {}).get("family") or "Arial"
    hl = str(sub.get("highlight", "primary")).strip()
    if hl in ("primary", "accent"):
        hl = color.get(hl) or "#FFD400"
    sub["highlight"] = None if hl == "none" else hl
    sub["zone"] = video.get("safe_zone") or DEFAULT_ZONE
    sub["box_bg"] = color.get("surface") or "#000000"
    return sub


# ---------- fonts ----------

def download_font(family, weight, folder):
    """Tries to download the font from Google Fonts as .ttf. If it can't, libass uses a similar one."""
    if not family or family.lower() in ("arial", "sans", "sans-serif"):
        return False
    os.makedirs(folder, exist_ok=True)
    url = "https://fonts.googleapis.com/css2?family=" + family.replace(" ", "+") + f":wght@{int(weight)}"
    try:
        # Without a browser user-agent, Google Fonts serves .ttf, which is what libass reads.
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
        css = urllib.request.urlopen(req, timeout=20).read().decode()
        ttf = re.search(r"url\((https://[^)]+\.ttf)\)", css)
        if not ttf:
            return False
        dest = os.path.join(folder, family.replace(" ", "") + f"-{int(weight)}.ttf")
        urllib.request.urlretrieve(ttf.group(1), dest)
        warn(f"font {family} {weight} ready at {dest}")
        return True
    except Exception as e:  # no network, or a family that isn't on Google Fonts
        warn(f"couldn't download {family} ({e.__class__.__name__}); put the .ttf in --fonts or install it.")
        return False


# ---------- transcribe ----------

def audio_16k(video):
    import numpy as np
    out = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(out, np.int16).astype(np.float32) / 32768.0


def transcribe(a):
    from faster_whisper import WhisperModel
    prompt = None
    if a.script:
        text = open(a.script, encoding="utf-8").read()
        spoken = re.findall(r'"([^"]{3,})"', text) or [text]
        prompt = " ".join(spoken)[:800]  # names and unusual words from the script help spell them right
    audio = audio_16k(a.video)

    def run(device):
        model = WhisperModel(a.model, device=device, compute_type="int8")
        segs, info = model.transcribe(audio, language=a.language, word_timestamps=True,
                                      vad_filter=True, initial_prompt=prompt)
        words = []
        for s in segs:  # transcription happens here; a GPU error surfaces in this loop
            for w in s.words or []:
                t = w.word.strip()
                if t:
                    words.append({"w": t, "s": round(w.start, 3), "e": round(w.end, 3)})
        return words, info

    try:
        words, info = run(a.device)
    except (RuntimeError, OSError) as e:
        # NVIDIA card without the CUDA libraries (cuBLAS, cuDNN): fall back to CPU, which always works.
        if a.device == "cpu":
            raise
        warn(f"the GPU isn't ready ({str(e)[:80]}); continuing on CPU.")
        words, info = run("cpu")
    json.dump({"language": info.language, "words": words,
               "text": " ".join(p["w"] for p in words)},
              open(a.output, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    warn(f"{len(words)} words in {a.output}. Check them against the script before burning.")


# ---------- burn ----------

def ass_color(hexa, alpha=0):
    h = hexa.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


def ass_time(t):
    t = max(0, t)
    h, rest = divmod(t, 3600)
    m, s = divmod(rest, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def srt_time(t):
    ms = int(round(max(0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def group(words, per_line, lines):
    cap = max(1, per_line * lines)
    groups, current = [], []
    for i, p in enumerate(words):
        current.append(p)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_of_sentence = p["w"][-1:] in ".?!…"
        pause = nxt is not None and nxt["s"] - p["e"] >= BREAK_PAUSE
        if len(current) >= cap or end_of_sentence or pause or nxt is None:
            groups.append(current)
            current = []
    return groups


def video_size(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", video],
                         check=True, capture_output=True, text=True).stdout.strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def burn(a):
    ds = read_ds(a.ds)
    if not ds:
        warn("no design-system.md: default style (white, black outline, 3 words, center).")
    st = style_from_ds(ds)
    w, h = video_size(a.video)
    scale = w / BASE_W  # the whole style is designed at 1080 wide
    size = round(st["size_px"] * scale)
    zy0, zy1 = [v * h / BASE_H for v in st["zone"]["y"]]
    block_h = size * 1.25 * st["lines"]
    y = {"top": zy0 + block_h / 2,
         "center": zy0 + 0.65 * (zy1 - zy0),
         "bottom": zy1 - block_h / 2}.get(st["position"], zy0 + 0.65 * (zy1 - zy0))
    zx0, zx1 = [v * w / BASE_W for v in st["zone"]["x"]]
    x = (zx0 + zx1) / 2

    fonts = a.fonts or os.path.join(os.path.dirname(os.path.abspath(a.output)), "fonts")
    download_font(st["font"], st["weight"], fonts)

    outline = st.get("outline") or {}
    border = round(float(outline.get("width_px", 6)) * scale, 1)
    border_style = 3 if st.get("box") else 1
    back = ass_color(st["box_bg"] if st.get("box") else outline.get("color", "#000000"),
                     0x30 if st.get("box") else 0)
    bold = -1 if int(st["weight"]) >= 600 else 0
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{st['font']},{size},{ass_color(st['color'])},{ass_color(st['color'])},{ass_color(outline.get('color', '#000000'))},{back},{bold},0,0,0,100,100,0,0,{border_style},{border},0,5,{int(zx0)},{int(w - zx1)},0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    data = json.load(open(a.transcript, encoding="utf-8"))
    words = data["words"]
    if st.get("uppercase"):
        words = [dict(p, w=p["w"].upper()) for p in words]
    groups = group(words, int(st["words_per_line"]), int(st["lines"]))
    per_line = int(st["words_per_line"])
    highlight = ass_color(st["highlight"]) if st["highlight"] else None
    events, srt = [], []
    for gi, g in enumerate(groups):
        group_end = g[-1]["e"] + 0.25
        if gi + 1 < len(groups):
            group_end = min(group_end, groups[gi + 1][0]["s"])
        for k, p in enumerate(g):
            start = p["s"] if k else g[0]["s"]
            end = g[k + 1]["s"] if k + 1 < len(g) else group_end
            parts = []
            for j, q in enumerate(g):
                t = q["w"].replace("{", "(").replace("}", ")")
                if j == k and highlight:
                    t = r"{\c" + highlight + "}" + t + r"{\c" + ass_color(st["color"]) + "}"
                parts.append(t)
                if j + 1 < len(g):
                    parts.append(r"\N" if (j + 1) % per_line == 0 else " ")
            text = "".join(parts).replace(r" \N ", r"\N")
            events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Sub,,0,0,0,,"
                          + r"{\an5\pos(" + f"{x:.0f},{y:.0f}" + ")}" + text)
        srt.append(f"{gi + 1}\n{srt_time(g[0]['s'])} --> {srt_time(group_end)}\n"
                   + " ".join(q["w"] for q in g) + "\n")

    base = os.path.splitext(a.output)[0]
    ass_path, srt_path = base + ".ass", base + ".srt"
    open(ass_path, "w", encoding="utf-8").write(header + "\n".join(events) + "\n")
    open(srt_path, "w", encoding="utf-8").write("\n".join(srt))
    warn(f"{len(groups)} blocks -> {ass_path} and {srt_path}")

    def esc_filter(r):
        return r.replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    vf = f"ass='{esc_filter(ass_path)}'"
    if os.path.isdir(fonts):
        vf += f":fontsdir='{esc_filter(fonts)}'"
    cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", a.video, "-vf", vf,
           "-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "copy", "-movflags", "+faststart", a.output]
    subprocess.run(cmd, check=True)
    warn(f"done: {a.output}")


def main():
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is missing. Install it: https://ffmpeg.org/download.html")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="step", required=True)
    t = sp.add_parser("transcribe", help="video -> transcript.json with per-word timestamps")
    t.add_argument("video")
    t.add_argument("-o", "--output", default="transcript.json")
    t.add_argument("--model", default="small", help="tiny | base | small | medium | large-v3 | turbo")
    t.add_argument("--language", default="en", help="ISO code of the spoken language (brand.language)")
    t.add_argument("--script", help="script .md: its words help spell proper names right")
    t.add_argument("--device", default="auto", help="auto | cpu | cuda (auto uses the GPU if it's ready, otherwise CPU)")
    b = sp.add_parser("burn", help="video + transcript.json -> video with subtitles")
    b.add_argument("video")
    b.add_argument("transcript")
    b.add_argument("-o", "--output", default="final.mp4")
    b.add_argument("--ds", help="path to design-system.md")
    b.add_argument("--fonts", help="folder with the subtitle font's .ttf files")
    b.add_argument("--crf", type=int, default=18)
    a = ap.parse_args()
    transcribe(a) if a.step == "transcribe" else burn(a)


if __name__ == "__main__":
    main()
