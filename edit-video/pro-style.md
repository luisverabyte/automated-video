# Pro editing: overlays, B-roll, sound and quality control

Reference for the `edit-video` skill at level 2. Read it when the video needs more than cuts, zoom, subtitles and music. Everything visual comes from design-system.md: `color`, `typography`, `shapes`, `motion`, `video` and `logo`. Wherever it says "your visual system", that's what it means.

This method came out of editing real videos with ffmpeg. The pieces of each step (rendering HTML with alpha, face tracking, compositing) are put together by the assistant with whatever you have installed; there aren't ready-made scripts for everything, so always start with a 3-second sample before rendering the whole video.

## Visual style

**Continuity (above everything).** The creator and the graphics are both narrators; the viewer moves from one to the other without jumps. Every B-roll entrance and exit and every scene change grows from something on screen and returns to something that was already there (a container that becomes the next one, a shot that shrinks into a shape and comes back, an answer that changes inside the same bubble), with real motion blur. A principle, not a template. A shot to camera or a large frame that changes shape → regular shapes (rounded rectangle, pill).

**Transitions**
- A-roll → A-roll: clean jump cut with a margin of silence, no `xfade` or effect. The zooms bring the energy.
- A-roll ↔ B-roll: from something on screen. Proven approach: an element grows until it becomes the B-roll and shrinks back (HTML rendered to .mov with alpha), with no blur or scale-in. The seed depends on what's being said: question → bubble, comparison → 1st card, number → the stat's card, post → its card, concept → label or icon. Stock transitions only if there's no element to grow from. A jump in the A-roll under a B-roll isn't visible: use that.
- Event photos and videos: Ken Burns per photo, Push, Zoom-through, Mosaic, Card, Iris; `xfade` 0.4 s between similar shots, 0.15 to 0.2 s if the scene changes. The return to camera starts on the first frame used, never with a splice from the raw footage inside it.
- Light Leak: only on top of glass/translucent layers, never as a cut.

**Motion**: nothing enters, leaves or sits still abruptly (soft entrances, a slight breathing motion, animated exits). A change of content is a change of state within the same render. One lead element moving at a time, small amplitudes. Fades: overlay 0.2 s, B-roll 0.3 s.

**Zoom**
- Between shots: 100/110% jump.
- Within a shot: continuous zoom at a constant speed toward the face without pushing it out of frame (face detection with OpenCV/MediaPipe; cap around 1.45). On a tripod, cut into sections with alternating 35 to 45% zoom on sections longer than 5 s.
- On emphasis shots, a stock zoom (slow Push In, stepped Punch-In, Pull Back Reveal, gentle Camera Shake) **replaces** the continuous one; never both.
- With an overlay or a background layer: low zoom (around 1.12) and no stock zooms.
- Event photos 12%, videos 8%, alternating in and out.
- Overlays and the cover get no zoom, timed on top of the already-zoomed cut.

**Kinds of support** (pick per sequence and mix). Zoom is the floor, not the plan. The creator stays at the center: full frame or in a frame for at least ~70% of the video, never two B-rolls in a row without coming back to them. In videos of 30 s or more, at least 3 kinds of support besides zoom, and none covering the whole video.

| The sequence… | Support options |
|---|---|
| Opinion, take, hook, close, joke to camera | Their shot + zoom (stock zoom if it's emphasis) |
| Names a company, person, number, post or study | Overlay with the real thing (logo, screenshot, source), a layer behind them, animated text |
| Points with a hand or talks about something "here" | Card next to what they point at, or a background layer |
| Shows a screen, chat or document | Low card (face on top), B-roll with them in a frame, a chat that types itself |
| An idea with steps: process, comparison, before/after | Continuous stretch: they shrink into a card and come back |
| Something you need to SEE (product, place, scene, diagram) | Full-screen B-roll |
| A vs B | Two cards that change state, or a split screen |
| The word that IS the video's concept | Text in the background behind their silhouette |

- Top overlay: HTML rendered with alpha and composited with ffmpeg, in the overlay band.
- Background layer: cards on the wall **behind their silhouette** (segmentation mask) with parallax. 3 max, never over the face, leaving at least 0.3 s before a cut; if they cover more than ~40% of the frames, shorten them.
- Continuous stretch: 8 to 20 s as one composition with their shot as a layer, for an idea with steps. Boundaries on shot jumps. Never the whole video.
- Letter-by-letter animated text: one keyword or number with motion inside an overlay or B-roll; one focal point per screen.
- Full-screen B-roll when the sequence calls for it, or with their face in a narrator frame: their shot shrinks into a frame inside the safe zone, without covering text or subtitles, and grows back on the way out. It's the preferred way into a long B-roll (over ~4 s). No image shorter than 1 s (except the cover).
- Third-party templates or libraries: repaint them with your visual system and make a 3-second sample before the first use.

**Recap** (an experience with your own footage): intro and close to camera; in the body, full-screen photos and videos right as each part is named; top overlays with the day, the name and the details being said. Horizontal or 3:4 photos shown whole over a blurred copy of themselves.

## Audio

- Never cut right against a word: up to 1 s of silence on each side; if the gap is shorter, don't cut there. Cut points by audio energy, not by Whisper's timestamps (the end of a word arrives before the real audio, after a long pause the start comes out 0.3 to 0.5 s early, and in noise it invents words).
- Removing a line: A = real end of the last word that stays + ~0.2 s; B = start of the next one − ~0.45 s, both below -35 dB.
- Only remove: lines they don't want, the opening silence (≤ 0.3 s) and the ending (+ ~0.6 s), and the middle of long pauses. Micro-pauses stay.
- If your subtitle tool trims pauses on its own: give it the composite with **every pause ≤ 0.45 s at -35 dB**, at least 0.2 s of silence on each side, and no fades over long pauses.
- Some phones record audio that drifts against the video: check the sync; cut with `-ss` on the container, never with `aresample=async`.

## Sound effects

- **Where they play** (one effect per event; never two whooshes at once; a click within 0.3 s of another sound is one too many): whoosh when a card, large overlay or B-roll enters and leaves; soft click when an option lights up; pop on a label; swipe on a change of state; bell when an idea lands. A-roll jumps get no sound.
- **Timing**: the cues come out of the same script that generates the overlays, in composite time, so sound and image move together if something changes.
- **Free sources, no generative AI**: your own synthesis or a library with a commercial license.
- **Level** against the voice in that window (RMS ~350 ms): whoosh ≈ 8 to 10 dB under the voice, clicks and pops ≈ 10 to 14 dB under the local peak. The mix doesn't change the voice's peak or integrated LUFS. One single master volume knob.
- **Mix**: voice from the cut + effects → wav → mux onto the composite with `-c:v copy`. Measure the peak per channel.

## Color and quality

- `ffprobe` every raw clip: if it's 1080p, warn (quality ceiling); if it's HDR (`arib-std-b67`/HLG), convert to SDR with tonemapping.
- Everything in **SDR bt709** (`-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`); the cover too (SDR cover + HLG video = oversaturated).
- Work at 120% and scale down to 1080x1920 with lanczos. Composite encoded **once**: `libx264 -crf 12 -preset slow -tune film -profile:v high -pix_fmt yuv420p` with `-t` = exact length.

## Full quality control

Everything passes before showing or uploading:

- loudness and true peak ≤ -1 dBTP; frozen or black frames; each overlay's box against the safe zone;
- a frame grid at each transition to B-roll, each A-roll jump and the last frames (no frames from another take and nothing over the subtitle band);
- a safe-zone guide over one frame per overlay, card and B-roll (at the end of its zoom);
- pauses ≤ 0.45 s at -35 dB and no splice clips a word;
- sync of the cut against the raw footage;
- sound: voice in the mix aligned with the cut's voice (offset 0), peak < -1 dBFS per channel, LUFS equal to the voice alone, each effect ≥ 8 dB under the voice in its window;
- skin and background as in the raw footage.
For review: MP4 1080x1920, `-crf 21 -preset medium`, aac 128k, `+faststart`; crf 12 is the master. To review on a phone: 720x1280, crf 26 to 28, ≤ 15 MB.

## Experiment log

Every video adds at least one rarely used or new device and doesn't feel the same as the previous one. Keep `videos/EXPERIMENTS.md` (device, video, result), read it when planning and add the row when delivering.

## If you use an external subtitle tool (OpusClip, Submagic, CapCut)

Optional: the skill already burns subtitles for free. If you prefer a tool that charges per project:

1. **Projects cost money**: if your subtitle tool charges per project, upload only the final version. A one-off mistake in the raw footage gets patched (corrected subtitle with an asterisk: "word*"). With **several** (a word that changes the meaning, missing lines, a different ending, a stat without its caveat): don't upload; report the list, the patch and what to re-record.
2. A new project loses the manual tweaks of the previous one: warn first and bundle all the changes into one version.
3. Upload only once the creator approves the composite, with no auto-trimming and with a subtitle template made from their design system. If the tool trims pauses on its own, give it the composite with every pause ≤ 0.45 s at -35 dB.
4. Correct the transcript in the tool (same number of words per replacement) and check: same length as the composite, last words complete, subtitles not covering overlays and the first frame matching the cover.
