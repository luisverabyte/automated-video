# Shared format: `design-system.md` (v1)

This is the contract between the skills in the kit. The **design-system** skill writes it; **video-script**, **edit-video** (with subtitles) and the bonus **teleprompter** read it. If a skill needs a brand detail, it looks for it here and nowhere else.

## Contract rules

1. **One file**, `design-system.md`, in Markdown. It works in any AI: upload it as a file, keep it in a Project or paste it at the start of the chat.
2. **Two layers.** A YAML block with the values (what machines read) and prose sections with the rules (what people and models read). Values live only in the YAML; the prose never repeats hex codes or sizes.
3. **Fixed keys.** Key names and `##` headings are never renamed. A skill that reads the file can rely on them.
4. **Nothing empty.** If the person didn't know what to answer, the skill proposes a value and tags it with `# proposed` at the end of the line. That tells the other skills they can suggest changes.
5. **Version.** `format: design-system-v1` in the YAML. If the contract changes, it moves to `v2` and the skills warn when they read a version they don't know.
6. **Optional derivatives.** Where files can be written (Claude Code, Cowork), the skill can generate `tokens.css` from the YAML. The `.md` stays the source of truth: if a value changes, change it there and regenerate.

This is the English edition of the kit. The Spanish edition ([video-automatico](https://github.com/luisverabyte/video-automatico)) uses the same structure with Spanish key names, so a file made with one edition is read by the skills of that same edition.

## How each skill reads it

| Skill | Reads | What for |
| --- | --- | --- |
| Video script | `brand`, `audience`, `voice`, `scriptwriting` and the "Voice" and "Scriptwriting" sections | Tone, words to use and avoid, length, structure, hook, close and off-limits topics |
| Edit video | `color`, `typography`, `shapes`, `motion`, `video`, `subtitles`, `logo` and the "Video" section | Overlays, colors, fonts, safe zone, watermark, music, effects and subtitle style |
| Teleprompter (bonus) | `color`, `typography`, `video.mode` | Colors and font of the recording page |

If a key is missing (for example, in a hand-made file), the skill uses the default from the table below and says so in one line.

## Template

Exact copy of what the skill delivers. The `#` comments explain each key and its valid values.

````markdown
# Design system: <brand>

```yaml
format: design-system-v1
updated: 2026-11-25               # YYYY-MM-DD

brand:
  name: ""                        # the brand's or person's name
  handle: ""                      # @username on social media, if any
  what_you_do: ""                 # one sentence: what you do and for whom
  promise: ""                     # what followers walk away with
  language: en                    # ISO code; all copy comes out in this language
  variant: neutral                # neutral | us | uk | au | ca | in | ... (local slang allowed)

audience:
  who: ""                         # role or situation, not age
  problem: ""                     # what hurts or what they want to achieve
  level: intermediate             # beginner | intermediate | advanced

voice:
  personality: []                 # 2 to 4 adjectives
  register: casual                # casual | neutral | formal
  humor: medium                   # none | light | medium | lots
  signature_phrases: []           # your own expressions that sound like the brand
  banned_phrases: []              # words or filler that are off-limits
  emojis: few                     # never | few | free

color:
  mode: light                     # light | dark | both (the first one is the main one)
  primary: "#000000"              # brand color: buttons, highlights, logo
  on_primary: "#FFFFFF"           # text on top of primary (contrast >= 4.5:1)
  background: "#FFFFFF"
  surface: "#F2F2F2"              # cards and blocks on the background
  text: "#111111"
  text_secondary: "#555555"
  accent: "#000000"               # occasional use, never the star
  dark:                           # only if mode is dark or both
    background: "#111111"
    surface: "#1C1C1C"
    text: "#EEEEEE"
    text_secondary: "#AAAAAA"
    primary: "#000000"
    on_primary: "#FFFFFF"
  banned: []                      # colors that are never used

typography:
  headings: { family: "", weight: 800, font_url: "" }   # font_url: Google Fonts or your own file
  body:     { family: "", weight: 400, font_url: "" }
  mono:     { family: "", weight: 500, font_url: "" }   # optional; empty if unused
  uppercase_headings: false

shapes:
  corners: rounded                # square | soft | rounded | pill
  radius_px: 24                   # card radius at 1080 px wide
  elements: []                    # signature shapes or devices (e.g. "circle", "hand-drawn underline")
  texture: none                   # none | grain | paper | glass | ...
  shadows: soft                   # none | soft | strong

logo:
  has_logo: false
  file: ""                        # path or file name, if it exists
  description: ""                 # what it looks like, if there's no file
  watermark: ""                   # text or logo; empty if none
  watermark_opacity: 0.35

motion:
  energy: medium                  # calm | medium | high
  entrances: soft                 # snappy | soft | bouncy
  transition_ms: 250

video:
  format: "1080x1920"             # vertical 9:16 by default
  mode: light                     # light | dark: background of overlays and cards
  safe_zone: { x: [120, 960], y: [270, 1250] }        # anything meant to be read goes inside
  platforms: []                   # tiktok | instagram | youtube | linkedin | ...
  duration_s: [30, 60]
  pace: medium                    # slow | medium | fast (cuts and zooms)
  music: soft                     # none | soft | featured
  sound_effects: few              # none | few | many
  broll: []                       # preferred visual support: screenshots, memes, photos, text...

subtitles:
  enabled: true
  font: ""                        # empty = typography.headings
  weight: 800
  size_px: 64                     # at 1080x1920
  color: "#FFFFFF"
  highlight: "primary"            # the word being spoken: primary | accent | hex | none
  outline: { color: "#000000", width_px: 6 }
  box: false                      # true = background behind the text
  position: center                # top | center | bottom (always inside the safe zone)
  words_per_line: 3
  lines: 1
  uppercase: false
  emojis: false

scriptwriting:
  structure: hook-body-close      # or the name of your own formula
  hook: ""                        # how you like to open (question, stat, contradiction...)
  close: ""                       # how you close; the CTA, if any
  topics: []                      # what you talk about
  banned_topics: []               # what you never talk about
  sources: verify                 # verify | free (verify = every fact has a source)
```

## Who it is and who it's for
Two or three sentences of prose with what doesn't fit in the YAML.

## Voice
Writing rules, with one example sentence that works and one that doesn't.

## Color
When each color is used. Banned combinations.

## Typography
Hierarchy and special uses.

## Shapes and logo
How shapes, the logo and the watermark are used. What is never done.

## Video
Editing style: what you like and what you don't. What overlays look like.

## Subtitles
The style in one sentence and a text sample: `THIS IS **KEY**`.

## Scriptwriting
Preferred formula, hook and close, with one example of each.

## Limits
What the brand never does or says.
````

## Defaults

A reading skill uses these when a key is missing. The design-system skill never leaves a key without asking or proposing.

| Key | Default |
| --- | --- |
| `video.format` | `1080x1920` |
| `video.safe_zone` | x 120 to 960, y 270 to 1250 (keeps clear of the TikTok, Reels and Shorts buttons and captions) |
| `subtitles.size_px` | 64 |
| `subtitles.words_per_line` | 3 |
| `subtitles.position` | `center` |
| `subtitles.highlight` | `primary` |
| `motion.transition_ms` | 250 |
| `voice.register` | `casual` |

Full example with a made-up brand: [`design-system/example/design-system.md`](design-system/example/design-system.md).
