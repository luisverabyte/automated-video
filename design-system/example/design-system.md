# Design system: Clear Cents

> Example with a made-up brand. Use it to see the full format and to try out the script and editing skills.

```yaml
format: design-system-v1
updated: 2026-11-25

brand:
  name: "Clear Cents"
  handle: "@clearcents"
  what_you_do: "I teach personal finance to people who just landed their first job"
  promise: "Know where your paycheck goes without endless spreadsheets"
  language: en
  variant: neutral

audience:
  who: "Professionals aged 22 to 30 with their first steady paycheck"
  problem: "They reach the end of the month with no idea where the money went"
  level: beginner

voice:
  personality: [warm, direct, funny]
  register: casual
  humor: medium
  signature_phrases: ["let's do the math", "zero guilt"]
  banned_phrases: ["financial freedom", "get rich", "invest now"]
  emojis: few

color:
  mode: light
  primary: "#1F7A5C"
  on_primary: "#FFFFFF"
  background: "#FAFAF5"
  surface: "#EEF3EC"
  text: "#18201C"
  text_secondary: "#4A5550"
  accent: "#E07A2F"
  dark:
    background: "#101513"      # proposed
    surface: "#1B2320"         # proposed
    text: "#E6ECE8"            # proposed
    text_secondary: "#A9B5AF"  # proposed
    primary: "#6FD3AE"         # proposed
    on_primary: "#00382A"      # proposed
  banned: ["bright red (reads as alarm or debt)"]

typography:
  headings: { family: "Nunito", weight: 900, font_url: "https://fonts.google.com/specimen/Nunito" }
  body:     { family: "Nunito Sans", weight: 400, font_url: "https://fonts.google.com/specimen/Nunito+Sans" }
  mono:     { family: "", weight: 500, font_url: "" }
  uppercase_headings: false

shapes:
  corners: rounded
  radius_px: 32
  elements: ["hand-drawn coin", "hand-drawn underline"]
  texture: grain
  shadows: soft

logo:
  has_logo: false
  file: ""
  description: "Pending. Direction: a coin with an open C, in primary"
  watermark: "@clearcents"
  watermark_opacity: 0.35

motion:
  energy: medium
  entrances: bouncy
  transition_ms: 250

video:
  format: "1080x1920"
  mode: light
  safe_zone: { x: [120, 960], y: [270, 1250] }
  platforms: [tiktok, instagram]
  duration_s: [30, 50]
  pace: fast
  music: soft
  sound_effects: few
  broll: [screenshots, animated text, original memes]

subtitles:
  enabled: true
  font: ""
  weight: 900
  size_px: 68
  color: "#FFFFFF"
  highlight: "accent"
  outline: { color: "#18201C", width_px: 6 }
  box: false
  position: center
  words_per_line: 3
  lines: 1
  uppercase: true
  emojis: false

scriptwriting:
  structure: hook-body-close
  hook: "A number from their own paycheck that stings"
  close: "One step you can take today, and the newsletter invite"
  topics: [budgeting, saving, credit card debt, first paycheck]
  banned_topics: [crypto, stock picks, politics]
  sources: verify
```

## Who it is and who it's for
Clear Cents talks to people who just got their first paycheck and feel the money slipping away. It doesn't sell investments: it teaches you to look at the numbers without fear.

## Voice
Like a friend who knows money and explains it over coffee. Short sentences, round numbers and zero guilt.
- Yes: "Let's do the math: 10 a day on delivery is 300 a month."
- No: "Discover the secret to achieving financial freedom."

## Color
The green primary marks what matters: buttons, key numbers and the underline. The orange accent only highlights one word or one figure per screen. Never bright red, not even for losses: use secondary text with an icon.

## Typography
Nunito 900 for hooks and big numbers; Nunito Sans 400 for everything else. Numbers always go in headings, never buried in a paragraph.

## Shapes and logo
Cards with 32 px corners and soft grain. The hand-drawn coin appears as a sticker in one corner, one per piece. Watermark: @clearcents bottom right, inside the safe zone.

## Video
Fast pace: cuts every 2 or 3 seconds and a slight zoom on the numbers. Screenshots of banking apps with the data blurred. Original memes, never third-party material.

## Subtitles
White uppercase with a dark outline, 3 words per line, centered. The word being spoken switches to orange. Sample: `YOUR PAYCHECK **VANISHES**`.

## Scriptwriting
Opens with a number that hurts ("40% of your paycheck goes to things you don't remember buying") and closes with one concrete step for today. Length: 30 to 50 seconds.

## Limits
Never promises returns, doesn't recommend stocks or crypto and never shows real bank details.
