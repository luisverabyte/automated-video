---
name: video-script
description: Writes short vertical video scripts (Reels, TikTok, Shorts) with the Storytelling Formula, the voice from your design-system.md, an A-roll/B-roll shot table, fun facts and fact-check notes. Use it when you ask for a script, video ideas or to turn a topic into a video.
---

# Short video script

## Before you start: your design-system.md

Look for `design-system.md` (format `design-system-v1`, created by the `design-system` skill) in the project folder, in the attachments or in the chat. Everything personal comes from there:

- **Main persona:** `audience` (who, problem, level) and the **Who it is and who it's for** section.
- **Language and tone:** `brand.language`, `brand.variant`, `voice` (personality, register, humor, `signature_phrases`, `banned_phrases`, emojis) and the **Voice** section.
- **How it's written:** `scriptwriting` (structure, hook, close, topics, `banned_topics`, sources), `video.duration_s` and the **Scriptwriting** and **Limits** sections.
- **Visual system** (for the "On screen" column): `color`, `typography`, `shapes`, `video.broll`.

A value tagged `# proposed` is used anyway, but you may suggest changing it. If a key is missing, use the default and say so in one line; never block. If there's no file, use all the defaults and suggest creating the design system:

| Key | Default |
|---|---|
| language | the conversation's |
| register | casual, like talking to a friend |
| humor | light, rather than sentimental |
| audience | people who want to apply the topic at work |
| scriptwriting.structure | Storytelling Formula (section 3) |
| scriptwriting.sources | verify |

What the creator says in the chat wins over the design system.

**Country and slang:** the skill assumes no country. Use `brand.variant` and the audience in `audience`. If they're missing, infer the country from how the creator writes; if it's still unclear, ask once. With an audience from several countries, neutral language and references that make sense across all of them.

**Delivery, in your AI's native format:** in Claude, as an artifact (or document) if available; in ChatGPT or Gemini, in Canvas; with file access, as Markdown in `scripts/<topic-in-kebab-case>.md`; if none of that exists, in the chat. Plus a short message.

## 0. What the viewer gets

This is the first step, before fact-checking or writing: the script starts from the person, not the topic. Read the main persona in the design system and answer:

1. **Their question:** what they'd ask about this topic, almost always "so what do I do with this?".
2. **The answer:** **"After watching this video, the viewer can ___"** with something they do, use or decide. Understanding the news or retelling it isn't enough.
3. **The creator's take answers it:** their opinion is the bridge between the topic and that answer. If it doesn't lead to something usable, propose the angle that does before writing.

Always for the main persona, news included. The creator picks the topic; this changes how it's told, not what's told. One video, one topic. If they ask for ideas, favor news; a timeless topic gets tied to something current (a news item, a launch).

Forms of value (one is enough): something they can do today (steps, a prompt, a setting), something they can use, a criterion to decide, a mistake they won't make again.

**Solved, never vague:** viewers don't want to think, they want the thing done. The advice says what to do, where (app, menu, button by its name) and how, with real material. If it takes more than one step, the video is that tutorial. Even better, a ready-made deliverable (template, prompt, file): propose one whenever the topic allows it.

**Realistic:** the advice fits how people actually work. A feature the tool already has beats a new habit nobody will keep.

- The hook promises that result, in the viewer's words.
- The payoff delivers it, said out loud and on screen (the prompt, the criterion, the steps).
- **Document, don't create:** favor the creator's real examples (their work, their screens, what happened to them) over abstract explanations or made-up examples. If you don't know which one they have, ask.
- If there's a demo, use real material with a visible mark (circle, arrow) on the key detail.
- The promise doesn't overreach: the video delivers all of it.
- The resource goes in the caption. "Comment X and I'll send it to you" only if the creator approves.

## 1. Fact-check

- With `scriptwriting.sources: verify`, every third-party name, date, company and number is checked on the web. If you can't search, mark it "to verify" in the notes.
- Anything false, doubtful or outdated in the creator's material stays out; tell them why.
- A fact you can't find isn't made up: the sentence goes without it and you note it.
- What the creator tells from their own experience isn't fact-checked. It goes in first person, without exaggerating.
- Keep opinion apart from facts: first person is enough; "for me" only if it could be read as a fact.

## 2. Fun facts

Research 5 to 8 candidates from first-hand sources and present them to the creator; none goes into the script until they choose. Pick for surprise (it contradicts what people believe, or puts the serious next to the absurd), always harmless and related to the central idea. Each candidate: the joke in 25 words or fewer with the surprise at the end, plus its source. Order them from most to least surprising and say which one you recommend. If none gets a "wait, seriously?", say so.

The chosen one goes as a joke to camera, no graphics and no announcement. The rest stay in the Fact-check notes.

## 3. Storytelling Formula

1. **Payoff first** (process): start from the answer in section 0; the most important sentence is the take turned into something the viewer does, uses or decides. The video defends ONE central idea. If the idea opens several takes, propose a series (one video per take) and write the chosen one first. If `scriptwriting.structure` calls for another formula, use it with these same rules.
2. **Hook**: provocative; its only job is to keep them watching. In the first 3 seconds it promises the concrete benefit from section 0, which the payoff delivers no matter what; a news item or a stat alone isn't a hook. Straight to the result, with urgency; context goes in the setup. True and short. Start from what the viewer can do, not from how the tool works.
3. **Setup**: value first; who the creator is or what the thing is comes after, in one direct sentence. With news, right after telling it, a bridge sentence that brings it down to the viewer ("What does this mean for you?").
4. **Trigger + conflict, as one idea**: the problem with a verifiable anchor (year, number, fact) and why the obvious solutions fail.
5. **Climax**: the solution, direct, opened with a connector that carries on from the conflict ("But…").
6. **Payoff**: the most important sentence and the delivery on the promise; no "follow me", "shout-out" or endings about the creator. Before it, if possible, a before/after you could draw as a chart. Close with a one-line recap or a quick step to check it worked. If `scriptwriting.close` defines a call to action, it goes after the payoff, never in its place.
7. **Loop (optional)**: the first words complete the last sentence, or a callback to an exact word or image from the hook. Never forced.

The story is true, personal and, if it fits the creator, funny. Never make up the creator's anecdotes: ask them or leave an optional, marked gap.

**"Result" format** (how-to or tool topics; same parts): hook = the result ("Make your own [famous thing] with AI"); setup = why it's worth it; trigger + conflict = the twist or the common mistake; climax = demo with real material, 3 to 5 screens, one idea and one mark per screen, the creator visible in a frame; payoff = the takeaway and their take. If the topic calls for another shape, the topic wins.

## 4. Writing

- **Shorter is better**: one short sentence per part whenever possible.
- **Only what serves the take**: a stat, quote or curiosity that doesn't push the central idea goes to the caption, another video or out.
- **Everything you plant pays off**; if it doesn't come back, cut it.
- **Every fact, grounded**: after each fact, what it means for the viewer, varying the phrasing.
- **One concrete everyday example**, like a task the person repeats.
- **Don't announce the structure** ("Fun fact:", "The solution?").
- **No literal translations** from another language and no jokes that only work in another language.
- **No template formulas** (quotas of "you", lists of three, forced build-ups).
- **Don't estimate length** from the word count; if the text looks much longer than `video.duration_s`, cut.
- **Respect the voice**: use `voice.signature_phrases`, never `voice.banned_phrases`, and nothing from **Limits** or `scriptwriting.banned_topics`.
- **No text that sounds like AI**: em dashes, "it's not X, it's Y", "in a world where", rhetorical-question endings.
- **In the creator's words**, not technical synonyms; a term the audience doesn't know gets swapped for simple words.
- **References the audience knows**: companies, products and places they recognize based on where they are (`brand.variant`); an unknown reference is no anchor.
- **Time from publication day**: if it goes out the day it happens, say "today" even if it's recorded earlier.
- **One spoken flow**: each part opens with a connector that carries on from the previous one, with no structure labels.
- **Define only what the central idea needs**, right after naming it; secondary things go as on-screen text or in the caption.
- **Name only what the viewer will use or see**, at the moment you explain it.

## 5. File format

Header: format, what the viewer walks away with (section 0), hook, payoff and loop if there is one. Then one section per part with its table:

```
## Trigger

| Shot | What you say | On screen |
|---|---|---|
| B-roll | "…" | … |
```

- **A-roll**: the creator to camera, with text or logos on top (each logo as its name is said). Used for opinions, fun facts and the final line.
- **B-roll**: a scene with their voice over it; "On screen" says which element it grows from and what it returns to.
- Hard data or a quote: source in small text, no URLs.

At the end, **Fact-check notes**: each fact with a linked source, what was corrected or left out and why, the fun fact candidates and any rights warnings.

## 6. On screen

The viewer moves from the creator to the graphics without jumps.

- **Every B-roll grows from something on screen and returns to something that was already there**; if there's no seed, plant one earlier (overlay or label).
- **Between shots to camera, no cut effect**; editing decides the zooms.
- **A shot to camera that changes shape: regular shapes only** (rounded rectangle, pill).
- **Visuals in HTML / your own graphics by default**. Stock only for a real scene a graphic can't explain. **No generative AI** without the creator's approval.
- **Visual humor** with original parodies, no copyrighted material.
- **The creator's own product or company**: name and official logo when it's said, plus one value line taken from their site; the link goes in the caption.
- **Screen-recorded tutorial**: screen and webcam with their narration, in sync. The narration is one more take in the script ("Tutorial"), trimmed to the steps; the teleprompter only carries what goes to camera. Face in a frame, a zoom on each click with a visible mark and, if the interface is in another language, a translated label next to each button.
- **Screen topics**: screenshots, not video. Include a table of zones and "What I need from you" (full screenshot plus one close-up per zone). Blur paths with a username, private data and anything in testing, and say so. If they talk to camera and to the screen: hook, setup and close to camera.

Devices (mix them; reusing is fine):
1. **Overlay above the creator**: the usual one; often the seed of what comes next.
2. **Background layer**: cards on the wall behind them, during consecutive lines to camera. Layer or zoom, never both.
3. **B-roll that grows from an element**: expands to full screen and comes back.
4. **Continuous stretch**: 8 to 20 s for an idea with steps; the creator shrinks into a card, the elements travel and they come back. One per video at most.
5. **Full-screen B-roll** when the sequence calls for it, or with the creator in a frame as narrator.

Everything uses the design system's visual system (`color`, `typography`, `shapes`).

## 7. Delivery

Silent review: does the main persona end up with something they do, use or decide, said and on screen in the payoff? Is the benefit in the first 3 seconds? Does every fact say what it means for the viewer? Is there an everyday example? Does it close with a recap or a check step? One central idea? A trigger with an anchor? Does every B-roll say where it grows from and where it returns? Does everything planted pay off? Is anything padding? Does any sentence sound translated?

Logic test (Barbara Minto's Pyramid Principle), silently; flag without rewriting (on an approved script, only report):
1. The idea the viewer takes away fits in one sentence; if rebutting it takes two different objections, those are two ideas; a hook line that promises something else goes.
2. Each part answers the question the previous one left open.
3. The supports in a group fit under one plural, in order, without repeating.
4. For each sentence in the body, "so what?": if covering it changes nothing, it goes (a chosen fun fact stays).
5. No sentence claims more than its data.

Short message that opens with the viewer's question and what they walk away with; facts corrected or left out; hook and loop; the list of fun facts; what the logic test flagged, in one line; what you need from the creator.

Creator's changes: in the same file, reply in one or two lines. If a change is a preference that will repeat, suggest adding it to design-system.md.

When they approve the script, offer the teleprompter (`teleprompter` skill, bonus) and, after recording, the edit (`edit-video` skill).

---

Original kit "My videos, automated in 3 steps" by Luis Vera (@luisverabyte) · https://luisverabyte.com · MIT License: you can use and adapt it as long as you keep this credit.
