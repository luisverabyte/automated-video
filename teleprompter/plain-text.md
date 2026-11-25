<!--
How to use it in any AI (ChatGPT, Gemini, Copilot, Claude without skills…):
- Quick: copy everything below the line and paste it as the first message of the chat. Paste or attach your design-system.md too.
- So it always remembers: in ChatGPT create a Project or a GPT; in Gemini, a Gem; in Claude, a Project. Paste this text into the instructions and upload your design-system.md as a file.
-->

----------------------------------------------------------------

From now on, when I approve a script, you build its teleprompter following these instructions. If you can't create files, give me the full HTML in a code block so I can save it as .html and open it in the browser.

# Teleprompter to record a script

It's a bonus: recording with a teleprompter is optional. It helps if memorizing is hard for you or you want to say the script word for word.

Use it when the creator approves a `video-script` script ("approved", "let's record", "give me the teleprompter"); if it's not clear they approved it, ask. It's only for recording: the A-roll/B-roll shots don't show up.

## Text

- Source: `scripts/<topic>.md` (or the script in the chat), only the "What you say" column, word for word. If something needs fixing, tell the creator; don't change it silently.
- One single take, in script order, with small labels for each part (Hook, Setup, Trigger, Conflict, Climax, Payoff).
- **Loop:** the closing line goes at the end in full, with the words that open the video in the edit highlighted. They aren't repeated at the start: it begins with what follows them in the hook.

## Build

1. One self-contained HTML page (inline CSS and JS), dark background, large centered text, with these controls:
   - auto-scroll with adjustable speed;
   - font size;
   - mirror mode (for a physical glass teleprompter);
   - back-to-top button and space bar to pause;
   - screen always on (Wake Lock API);
   - remember speed and size in `localStorage`, with a per-video prefix on the keys.
   Start from `template.html` (in this skill's folder): it already has all of that. Change only what's marked `CHANGE`: `<title>` ("Teleprompter <short topic>"), the header, the lines, the `localStorage` prefix and, from your design-system.md, the dark mode colors (`color.dark.*`, `color.accent`) and the `typography.body` font. Without a design system, keep the template's values.
   If you can't read files, write the full page with those same controls.
2. Save it as `scripts/teleprompter-<topic>.html` and deliver it in your AI's native format so it can be read while recording: in Claude, as an artifact; in ChatGPT or Gemini, in Canvas with preview; if none of that exists, the full HTML to save and open in the phone's or tablet's browser. If one already exists for that video, or there are changes (to the script first), update that same one.

## Delivery

Short message with the link or path and, if there's a loop, which words from the end get cut for the opening. Don't touch the script (the close stays at the end so the structure can be approved) or the `video-script` skill.

---

Original kit "My videos, automated in 3 steps" by Luis Vera (@luisverabyte) · https://luisverabyte.com · MIT License: you can use and adapt it as long as you keep this credit.
