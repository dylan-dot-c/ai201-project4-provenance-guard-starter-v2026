# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard takes a piece of writing and returns a guess about whether AI wrote it, a confidence score, a plain-English label, and a way to appeal. Here's the path a submission takes:

1. **The route (`app.py::submit`)** receives a JSON body with `text` and `creator_id`. It checks the input before anything else runs: a body that isn't a JSON object, a missing or empty `text` or `creator_id`, or fewer than 5 words gets a `400`. Text over 20,000 characters isn't refused: it's split into ~2,000-character chunks (up to 10, evenly sampled), and each signal's score is averaged across them. Only text over 500,000 characters gets a `413`. Each rejection is also written to the audit log.
2. **Signal one (`detector.py::model_signal`)** runs gpt2 locally and measures how predictable the text is (its perplexity). The result is squashed onto 0–1, where higher means more AI-like.
3. **Signal two (`stylometry.py::style_signal`)** measures the shape of the text without reading it: how much sentence length varies, how varied the vocabulary is, and how much expressive punctuation there is. It also returns a 0–1 score where higher means more AI-like.
4. **The combining rule (`scoring.py::combine_signals`)** turns the two scores into one confidence score. It uses a weighted average, then pulls the score toward 0.5 when the two signals disagree.
5. **The label mapping (`scoring.py::score_to_label`)** turns that number into a guess (`human` / `unsure` / `ai`) and the full sentence a writer sees.
6. **The audit log (`audit.py::log_decision`)** writes a new `content_id`, the creator, both signal scores, the combined score, the guess, the label, and `status: decided` to `logs/audit.jsonl`.
7. **The response** sends all of that back as JSON. If the writer disagrees, they `POST /appeal` with the `content_id` and their reasoning. That appends an `under_review` entry next to the original decision without overwriting it.

**Stretch feature added:** `GET /content/<id>` returns one item's current status, its original decision, and any appeals.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** Perplexity under gpt2, meaning how easy each next word was for a language model to guess. A perplexity of 45 maps to 0.5. Lower perplexity gives a higher (more AI-like) score.

**Why that might differ between human and AI writing:** A language model writes by picking likely next words, so its output is text a model finds easy to predict. People make odder, more specific choices.

**What it can't see:** Predictable is not the same as machine-written. Plain writing in short sentences with common words scores as AI-like. That covers second-language writers, younger writers, and anyone writing simply on purpose. My plain human test paragraph scored **0.897**, _higher_ than my clearly-AI paragraph (0.862). It also misses AI text that was prompted to use rare words, and ornate human prose scores as very human whoever wrote it.

### Signal two — the style signal

**What it measures:** Three things, each scaled to 0–1 "human-ness" between a floor and a ceiling, then combined and flipped so that higher means AI:

| Measure                | How it's computed                                                                                            | Floor → ceiling | Weight |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ | --------------- | ------ |
| Sentence length spread | stdev / mean of words per sentence                                                                           | 0.20 → 0.70     | 0.45   |
| Vocabulary variety     | unique / total words, first 150 words only                                                                   | 0.55 → 0.80     | 0.30   |
| Punctuation density    | commas, semicolons, colons, dashes, brackets, quotes, `?`, `!`, ellipses per 100 words (full stops excluded) | 4 → 14          | 0.25   |

Texts under 60 words are pulled toward 0.5 in proportion to their length, because there isn't enough text for these measures to mean much.

**Why that might differ between human and AI writing:** Generated prose tends to have even, mid-length sentences and tidy punctuation. Human writing is lumpier: a three-word sentence next to a long one, plus asides in dashes and brackets.

**What it can't see:** It can't read. Anything that changes the shape without changing the substance moves it: splitting or merging sentences, adding dashes or typos, pasting in a quote. It also punishes the same plain writers signal one does. My plain human paragraph has evenly sized short sentences and no punctuation besides full stops, so it scored **0.805**.

### The combining rule

**The rule:**

1. Take a weighted average of the two signals.
2. If the signals are more than 0.35 apart, they disagree, so the score is pulled halfway back toward 0.5: `score = 0.5 + (score − 0.5) × 0.5`. Two methods disagreeing is uncertainty, and uncertainty should land in "unsure", not become an accusation.

**The numbers** (in `config.py`): `WEIGHT_MODEL_SIGNAL = 0.6`, `WEIGHT_STYLE_SIGNAL = 0.4`, `DISAGREEMENT_GAP = 0.35`, `DISAGREEMENT_DAMPING = 0.5`, `HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.72`. The model signal gets more weight because it separated my calibration inputs more widely. I raised the AI threshold from the starter's 0.65 to 0.72 so the AI label needs stronger evidence than the human one.

**Where it lives:** `scoring.py::combine_signals`

**Calibration (Milestone 4):**

| Input                         | model_score | style_score | combined | label                   |
| ----------------------------- | ----------- | ----------- | -------- | ----------------------- |
| Clearly AI                    | 0.862       | 0.595       | 0.755    | ai                      |
| Clearly human                 | 0.310       | 0.021       | 0.194    | human                   |
| Plain, ordinary human writing | 0.897       | 0.805       | 0.860    | **ai (false positive)** |
| Lightly-edited AI             | 0.707       | 0.639       | 0.680    | unsure                  |

The plain human paragraph is the important finding. Both signals score it as _more_ AI-like than the real AI text, so no weighting of these two signals can fix it, and no threshold can either without also letting the clearly-AI text through. That's why the AI label tells the writer the check can be wrong about plain writing and points them to the appeal.

**A case where my two signals split, and what my rule does with it:**

> "Honestly? I have no idea what happened at the meeting. Someone yelled; someone else left. Then the projector died -- of course -- and we all just sat there, staring at the blank wall, like it owed us an explanation!"

model_score **0.595** (common words, leaning AI) vs style_score **0.183** (lumpy sentences and lots of punctuation, clearly human). The gap is 0.41, which is over 0.35, so the weighted average of 0.430 is pulled toward 0.5 and lands at **0.465 → unsure**. The model signal alone would lean AI. The rule treats the disagreement as uncertainty instead.

---

## Label Variants

| Label                 | Score range | The exact text a reader sees                                                                                                                                                                                                                                                        |
| --------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| high-confidence human | 0.00 – 0.35 | We think this was written by a person. Our automated check found the kind of variety in wording and rhythm that people's writing usually has.                                                                                                                                       |
| unsure                | 0.35 – 0.72 | We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces. |
| high-confidence AI    | 0.72 – 1.00 | Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.       |

Exactly 0.35 is "human" and exactly 0.72 is "ai" (`score_to_label` uses `<=` and `>=`). Every score from 0 to 1 maps to one label. All three were reached in testing (see the calibration table above).

> **Unit 8:** the AI threshold is now **0.76**, so `unsure` covers 0.35–0.76 and `ai` covers 0.76–1.00. This was the one improvement; see [The Improvement](#the-improvement). The unit 7 numbers above are left as they were when submitted.

**Why I worded the "unsure" one this way:** Most people who see it will have written their piece themselves, so it says plainly that it isn't an accusation and that nothing has happened to their work. It also gives a reason that doesn't blame them: checks struggle with short or plain writing.

---

## Sample Run

**A submission** (the plain human paragraph, which gets the false positive)

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I went to the store today. I bought milk and bread. The store was busy. I saw my friend there. We talked for a few minutes. Then I went home and made lunch. I made a sandwich with the bread. It was good. After lunch I watched TV for a while. Then I did my homework.", "creator_id": "dylan"}'
```

```json
{
  "confidence": 0.8601,
  "content_id": "d02fd345-996f-4a7c-918a-fce9e76ad88a",
  "creator_id": "dylan",
  "guess": "ai",
  "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
  "model_score": 0.897,
  "status": "decided",
  "style_score": 0.8048
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "d02fd345-996f-4a7c-918a-fce9e76ad88a", "reasoning": "I wrote this myself for a journaling exercise. I write in short simple sentences on purpose."}'
```

```json
{
  "appealed_at": "2026-11-04T23:04:44+00:00",
  "content_id": "d02fd345-996f-4a7c-918a-fce9e76ad88a",
  "message": "Thanks, your appeal is recorded. A person will review this piece, and it's marked as under review until they do.",
  "original_guess": "ai",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8601,
      "content_id": "d02fd345-996f-4a7c-918a-fce9e76ad88a",
      "creator_id": "dylan",
      "guess": "ai",
      "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
      "model_score": 0.897,
      "status": "decided",
      "style_score": 0.8048,
      "timestamp": "2026-11-04T23:04:44+00:00"
    },
    {
      "content_id": "d02fd345-996f-4a7c-918a-fce9e76ad88a",
      "creator_id": "dylan",
      "event": "appeal",
      "reasoning": "I wrote this myself for a journaling exercise. I write in short simple sentences on purpose.",
      "status": "under_review",
      "timestamp": "2026-11-04T23:04:44+00:00"
    }
  ]
}
```

**Bad input** (each rejection is also logged as `event: rejected`)

| Request                          | Status | `error`                                                            |
| -------------------------------- | ------ | ------------------------------------------------------------------ |
| no `text`                        | 400    | `missing_text`                                                     |
| `text` is whitespace             | 400    | `missing_text`                                                     |
| body is `[1, 2]`                 | 400    | `body_not_json_object`                                             |
| `"hi there"`                     | 400    | `text_too_short`                                                   |
| 25,800 characters                | 200    | none (scored as 10 chunks, `"chunks": 10` in the response and log) |
| 600,000 characters               | 413    | `text_too_long`                                                    |
| appeal with unknown `content_id` | 404    | `unknown_content_id`                                               |

---

## How I Used AI

**Moment 1**

- _Identify the runs and the route of the labels_
- _A list of runs for each label_
- _What I changed:_

**Moment 2**

- _Help with the assignment_
- _Results and instrcutions to do_
- _What I changed:_

**Moment 3 (unit 8)**

- _What I asked:_ I used Claude Code to run the attack set and my five criteria, judge held/broke, extend `run_eval.py` to test the appeal path, and draft the diagnoses and write-up.
- _What it gave me:_ The runs, the results files, and a first draft of every unit 8 section. It also found that the unedited AI paragraph behind most evasion attacks already scored "unsure" (0.682), which changed how I read the evasion failures.
- _What I decided myself:_ I supplied my own ten pieces of writing for criterion 1 rather than letting it make them up. I chose to revise criterion 2 to a fixed pair instead of reconstructing lost texts, and to keep the 0.5 target. I picked FP03 as my worst failure for the breakout.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** **10 per minute, 200 per day** (`config.py`: `RATE_LIMIT_PER_MINUTE`, `RATE_LIMIT_PER_DAY`)

**Why those numbers and not others:**

- **10 a minute.** A real writer submits a piece, reads the label, maybe edits a paragraph and submits again. Even someone pasting chapters one after another rarely gets past a few a minute, since each check takes a second or two and they have to read the result. 10 leaves room for that with headroom to spare. A script mapping my thresholds wants hundreds of near-identical variations, and at 10 a minute that takes hours instead of seconds.
- **200 a day.** That covers a heavy day of revising, around 20 drafts of 10 pieces each. A script that waits out the per-minute window still gets stuck here: 1,000 variations would take five days from one caller.
- **Why not lower:** 5 a minute would trip a writer re-checking a few edits in a row, and a 429 after an honest edit feels like a punishment. **Why not higher:** at 30 a minute or more, a probe can sweep the whole 0.35–0.72 unsure band in a few minutes.

**What a caller counts as:** the `creator_id` in the body, falling back to the caller's IP address when there isn't one (`app.py::rate_limit_key`). This means one writer behind a shared school or office network isn't blocked by their classmates. The cost is that a script can make up a new `creator_id` for every request and never hit the limit. Every row in `attacks.csv` does exactly that. Per-address limiting would catch that script, but it would also lump a whole household or classroom into one caller.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15` → `results/flood_2026-11-04_1826.md`

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

The first 10 go through and the 11th onward get `429`. Each 429 is written to `logs/audit.jsonl` as an `event: rejected` entry by the 429 handler in `app.py`.

---

## Attack Run — Before

`python run_attacks.py --set attack_set --label before` → [results/attack_run_2026-11-11_1808_before.md](results/attack_run_2026-11-11_1808_before.md). 56 attacks, 0 crashes, 0 responses that weren't JSON.

**How I judged held or broke.** I used one rule per family, set before I filled in the table:

- **evasion** (AI text in disguise): HELD only if it's labelled `ai`. `unsure` counts as BROKE because the AI text went through without being flagged.
- **false_positive** (real human writing): HELD if it's _not_ labelled `ai`. `unsure` is fine because it isn't an accusation.
- **prompt_injection**: PI01–03 carry AI text, so they're judged like evasion. PI04–06 are HELD if the response, the label text and the log line come out uncorrupted and the human text isn't accused.
- **malformed / flood**: HELD if the service answers with JSON and a sensible status (no 500, no crash), and the flood is cut off at my limit.

| ID | Targeting | Status | Guess | model | style | combined | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | signal two: typos raise word variety | 200 | unsure | 0.164 | 0.700 | 0.439 | **BROKE** |
| EV02 | signal two: broken-up sentences | 200 | unsure | 0.594 | 0.250 | 0.457 | **BROKE** |
| EV03 | signal two: a pasted quotation | 200 | unsure | 0.666 | 0.416 | 0.566 | **BROKE** |
| EV04 | signal one: unusual words | 200 | unsure | 0.611 | 0.700 | 0.647 | **BROKE** |
| EV05 | both: heavy human editing pass | 200 | human | 0.321 | 0.258 | 0.296 | **BROKE** |
| EV06 | signal two: one very long + one very short sentence | 200 | unsure | 0.573 | 0.310 | 0.468 | **BROKE** |
| EV07 | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.482 | 0.545 | **BROKE** |
| EV08 | signal one: text below the token window | 200 | unsure | 0.245 | 0.521 | 0.356 | **BROKE** |
| EV09 | both: human opening bolted on | 200 | unsure | 0.704 | 0.447 | 0.601 | **BROKE** |
| EV10 | signal two: repeated stanza structure | 200 | ai | 0.979 | 0.826 | 0.918 | HELD |
| FP01 | plain, clear human writing | 200 | unsure | 0.618 | 0.578 | 0.602 | HELD |
| FP02 | human writing, formal register | 200 | **ai** | 0.739 | 0.771 | 0.752 | **BROKE** |
| FP03 | non-native English speaker writing carefully | 200 | **ai** | 0.805 | 0.677 | 0.754 | **BROKE** |
| FP04 | student essay written to a rubric | 200 | unsure | 0.833 | 0.550 | 0.7197 | HELD (by 0.0003) |
| FP05 | technical documentation by a person | 200 | **ai** | 0.801 | 0.888 | 0.836 | **BROKE** |
| FP06 | a person imitating a formal template | 200 | unsure | 0.881 | 0.491 | 0.613 | HELD |
| FP07 | human writing repeating a phrase on purpose | 200 | **ai** | 0.882 | 0.549 | 0.749 | **BROKE** |
| FP08 | very short genuine human submission | 200 | unsure | 0.322 | 0.499 | 0.393 | HELD |
| PI01 | instruction to ignore the check | 200 | unsure | 0.463 | 0.338 | 0.413 | **BROKE** |
| PI02 | instruction disguised as a system message | 200 | **human** | 0.204 | 0.337 | 0.257 | **BROKE** |
| PI03 | instruction in the writer's voice | 200 | unsure | 0.594 | 0.532 | 0.569 | **BROKE** |
| PI04 | make the label text hostile (`</label><script>`) | 200 | unsure | 0.500 | 0.438 | 0.475 | HELD |
| PI05 | inject fake fields into the audit log | 200 | unsure | 0.640 | 0.353 | 0.525 | HELD |
| PI06 | instruction plus real human text | 200 | unsure | 0.558 | 0.590 | 0.571 | HELD |
| MF01 | text is only whitespace | 400 `missing_text` | — | — | — | — | HELD |
| MF02 | single character | 400 `text_too_short` | — | — | — | — | HELD |
| MF03 | control characters | 400 `text_too_short` | — | — | — | — | HELD |
| MF04 | only punctuation | 400 `text_too_short` | — | — | — | — | HELD |
| MF05 | one very long word | 400 `text_too_short` | — | — | — | — | HELD |
| MF06 | emoji only | 400 `text_too_short` | — | — | — | — | HELD |
| MF07 | right-to-left (Arabic) script | 400 `text_too_short` | — | — | — | — | HELD (no crash, wrong reason, see below) |
| MF08 | 60,000 characters | 200, 10 chunks | ai | 0.988 | 0.777 | 0.904 | HELD (no crash, see below) |
| RQ01 | no text field | 400 `missing_text` | — | — | — | — | HELD |
| RQ02 | no creator_id | 400 `missing_creator_id` | — | — | — | — | HELD |
| RQ03 | text is a number | 400 `missing_text` | — | — | — | — | HELD |
| RQ04 | text is a list | 400 `missing_text` | — | — | — | — | HELD |
| RQ05 | text is null | 400 `missing_text` | — | — | — | — | HELD |
| RQ06 | creator_id is an object | 400 `missing_creator_id` | — | — | — | — | HELD |
| RQ07 | body is a JSON array | 400 `body_not_json_object` | — | — | — | — | HELD |
| RQ08 | unparseable JSON | 400 `body_not_json_object` | — | — | — | — | HELD |
| RQ09 | empty body | 400 `body_not_json_object` | — | — | — | — | HELD |
| RQ10 | form-encoded body | 400 `body_not_json_object` | — | — | — | — | HELD |
| RQ11 | JSON sent as text/plain | 400 `body_not_json_object` | — | — | — | — | HELD |
| RQ12 | deeply nested JSON | 400 `missing_text` | — | — | — | — | HELD |
| FL01_01–10 | 20 rapid submissions from one creator | 200 ×10 | unsure | 0.029 | 0.530 | 0.365 | HELD |
| FL01_11–12 | (same) | **429** ×2 | — | — | — | — | HELD |

**Count**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 4 | 4 |
| prompt_injection | 6 | 3 | 3 |
| malformed | 20 | 20 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| **Total** | **56** | **40** | **16** |

**A check I ran next to the attack set.** Eight of the ten evasions are edits of one AI paragraph, but the set never sends that paragraph unedited. I scored it directly with `detector.model_signal` and `stylometry.style_signal`: **model 0.669, style 0.700, combined 0.682 → unsure.** My system doesn't flag the _unedited_ AI text either. Seven of the nine evasion "breaks" were already through before the attacker changed a word. The edits only matter for EV05 and PI02, which pushed the text all the way to `human`.

**Ten audit log entries from the run** (raw lines from `logs/audit.jsonl`, plus one 429 and one route rejection)

```json
{"timestamp": "2026-11-11T23:08:44+00:00", "content_id": "44a080f5-9dcb-4900-aa59-c33bdc91afca", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6771, "combined_score": 0.7539, "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.", "status": "decided", "chunks": 1}
{"timestamp": "2026-11-11T23:08:45+00:00", "content_id": "44f97bb2-9fe4-47ea-8165-ae612072b6e1", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.888, "combined_score": 0.8355, "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.", "status": "decided", "chunks": 1}
{"timestamp": "2026-11-11T23:08:45+00:00", "content_id": "edb46fa8-7403-450d-9f63-43ccc2e95ab5", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.5492, "combined_score": 0.7486, "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.", "status": "decided", "chunks": 1}
{"timestamp": "2026-11-11T23:08:43+00:00", "content_id": "71852210-083c-4f75-bba3-e09e25fc8a24", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.2578, "combined_score": 0.2958, "label": "We think this was written by a person. Our automated check found the kind of variety in wording and rhythm that people's writing usually has.", "status": "decided", "chunks": 1}
{"timestamp": "2026-11-11T23:08:42+00:00", "content_id": "476517a3-ae4e-4368-ab5d-d54e5784cfa2", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.7, "combined_score": 0.439, "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.", "status": "decided", "chunks": 1}
{"timestamp": "2026-11-11T23:08:45+00:00", "content_id": "ca25d96f-4b32-4b42-b800-28876ededd15", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3367, "combined_score": 0.2573, "label": "We think this was written by a person. Our automated check found the kind of variety in wording and rhythm that people's writing usually has.", "status": "decided", "chunks": 1}
{"timestamp": "2026-11-11T23:08:46+00:00", "content_id": "2582c178-dc37-4053-8a8c-9b70e5409d33", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.3529, "combined_score": 0.5252, "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.", "status": "decided", "chunks": 1}
{"timestamp": "2026-11-11T23:08:50+00:00", "content_id": "10b84bf5-54c1-4d70-90a0-0ecf7ce4dd4a", "creator_id": "attacker_MF08", "guess": "ai", "model_score": 0.9878, "style_score": 0.7772, "combined_score": 0.9036, "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.", "status": "decided", "chunks": 10}
{"timestamp": "2026-11-11T23:08:46+00:00", "creator_id": "attacker_MF07", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
{"timestamp": "2026-11-11T23:08:50+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "missing_creator_id"}
{"timestamp": "2026-11-11T23:08:51+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

What these show:

- **FP03, FP05, FP07** are real people's writing called AI.
- **EV05** and **PI02** are AI text called human.
- **EV01** is the typo attack. It aimed at signal two but actually moved signal one: model_score fell to 0.16 while style stayed at 0.70.
- **PI05** shows the log-injection attempt failing. The fake `"guess": "human", "combined_score": 0.01` stayed inside an escaped string in the submitted text and never became a field, and the line is still one valid JSON object.
- **MF08** is 60,000 characters of a human camping paragraph repeated. It was chunked and scored without crashing, but it got `ai`.
- **MF07** is a real Arabic sentence refused as "too short".
- The last two entries are a route rejection with no creator (logged as `unknown`) and a rate-limit **429** from the flood rows.

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:

**FP03**, the non-native English speaker:

> I want to describe my experience of the first month in this country. The weather was very different from my home. I did not expect the rain to continue for so many days. My colleagues were kind and they helped me to find an apartment. [...]

It got **`ai` at 0.754** (model 0.805, style 0.677). This person is writing carefully in their second language, in short correct sentences with common words, and that care is exactly what got them accused. Both signals agreed, so nothing in the pipeline pulled the score back. The label tells them "checks like this can be wrong, especially about plain or simple writing". That is accurate, but it still reads as an accusation to someone already worried about fitting in.

---

## Run Log and Verdicts

`python run_eval.py --label before` → [results/run_2026-11-11_1833_before.md](results/run_2026-11-11_1833_before.md). Scenarios are in [scenarios.py](scenarios.py). Criterion 4 can't be tested by sending text alone, so I extended `run_eval.py` (`run_appeals`) to submit each piece, appeal its `content_id`, then read `GET /log` back and check that both the decision and the appeal are there.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 2 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. Clearly-AI vs clearly-human spread (revised, see `criteria.md`) | ≥ 0.50 apart | 0.545 | 0.545 | 0.545 | MET |
| 3. All three labels reachable across 15 pieces | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeals return `under_review` and are logged next to the decision | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Bad input gets a JSON response, no 500 | ≥ 8 of 10 | 10/10 | 10/10 | 10/10 | MET |

All three trials were identical, down to the fourth decimal place. Nothing in either signal is random, so this is expected. It shows the results hold rather than having turned up once.

**How I decided each verdict**

1. **MET.** Across all 30 trial results, none of my ten pieces was labelled `ai`: 9 were `unsure` and 1 was `human`. The highest score was 0.569.
2. **MET**, but narrowly. CLEARLY_AI scored 0.790 and CLEARLY_HUMAN scored 0.2454, so they're 0.5446 apart, which clears 0.5 by 0.045 in every trial.
3. **MET.** Every trial returned `ai` 6 times, `unsure` 8 times and `human` once. `human` was reached by exactly one piece, so this target holds by a single input.
4. **MET.** In all 30 cases the appeal response said `under_review`, and the log held both the decision and the appeal for that `content_id`.
5. **MET.** All 10 cases, in all three trials, got JSON back with no 500. There were eight 400s, one 200 for the ~28,000-character text (chunked and scored), and one 413 for the 600,000-character text.

**Were my targets too low?** Yes, at least for criterion 1, and that's the one I'd tighten. My ten pieces are informal notes full of typos ("thological", "hwole", "dong want jt"). Typos are rare tokens to gpt2, so they push perplexity up and signal one down: seven of my ten pieces got a model_score under 0.20. My writing passed *because* it's messy, not because the system protects plain writers. Two pieces of evidence show this. The plain paragraph I wrote for unit 7 ("I went to the store today...") still scores **0.860 → ai**; it's in the criterion 3 set. And the attack set's plain and formal human pieces were flagged 4 times out of 8. A tighter criterion 1 would read: "of 10 pieces I wrote myself, **at least 5 of them written plainly and carefully, without typos**, at most 2 labelled AI." I expect that one to miss. Criterion 3 also holds by a single input, and criterion 2 holds by 0.045.

**Real output from one trial.** This was produced by `run_eval.py::main` (and `run_eval.py::run_appeals` for criterion 4) against `app.py::submit`, and copied from the results file. The `label` sentence is left out of each row to save space; it's in full in the results file.

**my own writing** (trial 1)

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.3765, "model_score": 0.0437, "style_score": 0.5667, "sent": "research is cool but its mainly thological\n\nindustry/consulting is adv"},
  {"status": 200, "guess": "unsure", "confidence": 0.3794, "model_score": 0.0269, "style_score": 0.6067, "sent": "yh cause the hwole idea is based on synthtic AI questions and labels i"},
  {"status": 200, "guess": "unsure", "confidence": 0.5692, "model_score": 0.4362, "style_score": 0.7686, "sent": "How does it seem like im good at using computers where its nothing cra"},
  {"status": 200, "guess": "human", "confidence": 0.2454, "model_score": 0.172, "style_score": 0.3555, "sent": "lol I was also a consultant for the website I was building for my frie"},
  {"status": 200, "guess": "unsure", "confidence": 0.4213, "model_score": 0.0907, "style_score": 0.7206, "sent": "I think we might have to incorporate their google calendar where it sc"},
  {"status": 200, "guess": "unsure", "confidence": 0.3833, "model_score": 0.0376, "style_score": 0.61, "sent": "What id do is if my motivation or energy is really down bad it would s"},
  {"status": 200, "guess": "unsure", "confidence": 0.45, "model_score": 0.3122, "style_score": 0.6567, "sent": "Damn programming is so much lol\n\nIts good we have AI but its crazy\n\nTh"},
  {"status": 200, "guess": "unsure", "confidence": 0.4578, "model_score": 0.2586, "style_score": 0.6513, "sent": "Also it should use the least/max time needed for a project so a prject"},
  {"status": 200, "guess": "unsure", "confidence": 0.4156, "model_score": 0.1476, "style_score": 0.6067, "sent": "question about the abstract, we talk about synthetic evidence source l"},
  {"status": 200, "guess": "unsure", "confidence": 0.4333, "model_score": 0.1876, "style_score": 0.6349, "sent": "Conducted research on adult learning principles (andragogy) and best p"}
]
```

**calibration pair** (trial 1)

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.79, "model_score": 0.8713, "style_score": 0.668, "sent": "Effective leadership is a critical component of organizational success"},
  {"status": 200, "guess": "human", "confidence": 0.2454, "model_score": 0.172, "style_score": 0.3555, "sent": "lol I was also a consultant for the website I was building for my frie"}
]
```

**label coverage** (trial 1)

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.7454, "model_score": 0.8573, "style_score": 0.5776, "sent": "Artificial intelligence is transforming the way businesses operate. By"},
  {"status": 200, "guess": "ai", "confidence": 0.8078, "model_score": 0.9266, "style_score": 0.6295, "sent": "Regular physical activity offers numerous benefits for both physical a"},
  {"status": 200, "guess": "ai", "confidence": 0.7953, "model_score": 0.8437, "style_score": 0.7228, "sent": "Time management is an essential skill for success in both academic and"},
  {"status": 200, "guess": "ai", "confidence": 0.7232, "model_score": 0.8049, "style_score": 0.6007, "sent": "Remote work has become increasingly common in recent years. This shift"},
  {"status": 200, "guess": "ai", "confidence": 0.7249, "model_score": 0.8136, "style_score": 0.5919, "sent": "Reading is one of the most valuable habits a person can develop. It ex"},
  {"status": 200, "guess": "unsure", "confidence": 0.5763, "model_score": 0.6832, "style_score": 0.4159, "sent": "Remote work has become really common, and honestly I'm still not sure "},
  {"status": 200, "guess": "unsure", "confidence": 0.4952, "model_score": 0.6347, "style_score": 0.2741, "sent": "Exercise is good for you. Everybody knows that. What they don't tell y"},
  {"status": 200, "guess": "unsure", "confidence": 0.4195, "model_score": 0.5183, "style_score": 0.2712, "sent": "Time management is an important skill, and the main thing I've learned"},
  {"status": 200, "guess": "unsure", "confidence": 0.5609, "model_score": 0.6941, "style_score": 0.3612, "sent": "Reading is one of the best habits you can build, or so everyone keeps "},
  {"status": 200, "guess": "unsure", "confidence": 0.4652, "model_score": 0.5953, "style_score": 0.1833, "sent": "Honestly? I have no idea what happened at the meeting. Someone yelled;"},
  {"status": 200, "guess": "unsure", "confidence": 0.3765, "model_score": 0.0437, "style_score": 0.5667, "sent": "research is cool but its mainly thological\n\nindustry/consulting is adv"},
  {"status": 200, "guess": "unsure", "confidence": 0.3794, "model_score": 0.0269, "style_score": 0.6067, "sent": "yh cause the hwole idea is based on synthtic AI questions and labels i"},
  {"status": 200, "guess": "unsure", "confidence": 0.5692, "model_score": 0.4362, "style_score": 0.7686, "sent": "How does it seem like im good at using computers where its nothing cra"},
  {"status": 200, "guess": "human", "confidence": 0.2454, "model_score": 0.172, "style_score": 0.3555, "sent": "lol I was also a consultant for the website I was building for my frie"},
  {"status": 200, "guess": "ai", "confidence": 0.8601, "model_score": 0.897, "style_score": 0.8048, "sent": "I went to the store today. I bought milk and bread. The store was busy"}
]
```

**appeal path** (trial 1)

```json
[
  {"sent": "I wrote this paragraph about my weekend. We went hiking and it rained ", "submit_status": 200, "content_id": "9f9183cb-3929-4502-a891-c5f6aca6b028", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "My grandmother taught me to bake bread when I was ten. I still use her", "submit_status": 200, "content_id": "79696407-fc68-4720-b912-3dcf8311de44", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "The bus was late again this morning, so I walked the last mile and got", "submit_status": 200, "content_id": "afd08926-f84c-4fe5-99bb-b05f9ff6c222", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "Our team lost the final by one point. Nobody said much on the drive ho", "submit_status": 200, "content_id": "572ec57e-35d6-4405-bdc5-407a2a0e293b", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "I fixed the leaking tap myself after watching three videos and breakin", "submit_status": 200, "content_id": "130035dd-257d-491f-b4a2-94580e5f58d4", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "This essay argues that public libraries matter more now than they did ", "submit_status": 200, "content_id": "9740559f-6ab8-42bb-974e-4792befad9ac", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "The importance of effective communication in the workplace cannot be o", "submit_status": 200, "content_id": "57f7f3be-d208-44e5-974b-f0e5b3886069", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "We adopted a dog from the shelter last spring. She is afraid of the va", "submit_status": 200, "content_id": "1464e573-573e-4c7e-9e94-7ac27a67f001", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "I started learning guitar in March. My fingers hurt for a month and th", "submit_status": 200, "content_id": "7536ff6b-e000-4532-b9a1-c383c47dedd5", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true},
  {"sent": "The report recommends three changes to the timetable, set out in the f", "submit_status": 200, "content_id": "587577dd-e42d-47f3-a6dd-331644040c84", "guess": "unsure", "appeal_status": 200, "status": "under_review", "log_has_decision": true, "log_has_appeal": true, "passed": true}
]
```

**bad input** (trial 1)

```json
[
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "{\"creator_id\": \"eval_bad_missing\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "(empty text)"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "   \n\t  "},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "{\"text\": [\"a\", \"b\"], \"creator_id\": \"eval_bad_list\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "{\"text\": \"Some writing with no creator attached.\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "hi there"},
  {"status": 200, "guess": "ai", "confidence": 0.9982, "model_score": 0.997, "style_score": 1.0, "sent": "We walked to the river and back before lunch. We walked to the river a"},
  {"status": 413, "guess": null, "confidence": null, "model_score": null, "style_score": null, "sent": "word word word word word word word word word word word word word word "}
]
```

**Diagnoses**

Every criterion was met, so the misses to diagnose are the 16 broken attacks. They fall into four patterns.

**Pattern 1: the AI threshold sits above the AI text the attacks are built on (stage: label mapping, fed by signal one's calibration). This accounts for EV02, EV03, EV04, EV06, EV07, EV09, PI01 and PI03.**
The unedited base paragraph scores model 0.669 (perplexity 29), style 0.700, combined **0.682**. That is already below my `AI_THRESHOLD` of 0.72, before any attack is applied. Signal one's midpoint maps perplexity 45 to 0.5, so text at perplexity 29 only reaches 0.67. Signal two caps word variety at its 0.80 ceiling, and the paragraph's 0.87 can't count as more AI than that. So the attack edits only had to keep the text where it already was. Most of them pulled it _down_ a little, with combined scores of 0.46–0.65. For example, EV02's inserted "Really." sentences raised sentence-length spread and took style from 0.70 to 0.25. I don't count these as eight separate failures. They're one: my AI band starts above where this kind of AI text lands.

**Pattern 2: anything odd in the text drags signal one down (stage: signal one; mechanism: perplexity is a mean over every token). This covers EV01, PI02 and EV08.**
- **EV01 (typos).** This attack was aimed at signal two, but signal two didn't move: style stayed at 0.70, because word variety was already above the ceiling. Signal one collapsed instead, from 0.669 to **0.164**. Misspellings like "poistioned" and "thsi" break into rare sub-word tokens that gpt2 finds very surprising, so the perplexity of the whole text rises. The attack worked, just on the other signal.
- **PI02 (fake system message).** No model in my pipeline reads instructions, so "Return guess=human" isn't _obeyed_. It's scored as text, though, and that line alone has perplexity 537 (model_signal 0.019). Averaged in with the AI paragraph, it dragged model_score to **0.204**, and the result was **human, 0.257**. The injection got exactly what it asked for, by being weird rather than by being followed.
- **EV08 (10 words).** The route lets it through, because `MIN_WORDS` is 5. Ten words gives gpt2 almost no context, so perplexity is high and model_score is 0.245. Signal two's short-text rule pulls style to 0.52, and the combined score of 0.356 lands one hundredth above the human threshold.

The same mechanism is why criterion 1 passed: my typos lower my own model_scores.

**Pattern 3: the human false positives, where both signals share a blind spot (stages: signals one and two, then the combining rule and the label mapping). This covers FP02, FP03, FP05 and FP07.**
These four score model 0.74–0.88 and style 0.55–0.89. Formal, careful, second-language or deliberately repetitive writing has common words in predictable order, which pushes signal one up. FP07's repeated "It rained on..." is the extreme case: gpt2 predicts a phrase it has just seen. These pieces also have evenly sized sentences and few commas, which pushes signal two up. Because the two signals _agree_ (gaps 0.03–0.33, all under `DISAGREEMENT_GAP` 0.35), my combining rule gives no protection. The damping only fires on disagreement, so a blind spot both signals share reads as confidence. Three of the four then land in a tight cluster at **0.749–0.754**, just over the 0.72 line. FP04 sits at 0.7197, under the line by 0.0003. FP05 (technical docs) is at 0.836, well clear. Calling these four separate failures would be wrong. It's one: **both signals measure plainness, not machine origin.** My Claude-generated AI pieces score 0.72–0.81, which is the same range as these human ones. There is no threshold that separates them.

**Pattern 4: heavy human editing (stage: both signals, and correct by their own lights). This is EV05.**
EV05 was rewritten by a person, with asides, fragments, dashes and specific detail. Model 0.32, style 0.26, **human 0.296**. Both signals saw what they're built to see. By the time the editing is this heavy, the text arguably _is_ human writing, and I don't think a style-and-predictability detector should catch it. It still counts as a break against the family's goal.

**Not counted as breaks, but found in the run (route stage):**
- **MF07 (Arabic).** `stylometry.words` only matches `[a-z0-9']`, so a real Arabic sentence counts as 0 words and gets "Send at least 5 words". It doesn't crash, but the reason given is wrong, and anyone not writing in Latin script can't use the service at all.
- **MF08 and the criterion 5 long text.** Text repeated many times scores 0.90–0.998 → ai. Repetition is maximally predictable to gpt2 inside each chunk.

---

## The Improvement

**What I changed:** one number. `AI_THRESHOLD` in `config.py` went from **0.72 to 0.76**, which widens the unsure band to 0.35–0.76. Nothing else moved: same signals, same weights, same disagreement rule, same human threshold and same label text.

**Which diagnosis pointed at it:** Pattern 3. Three of the four human false positives (FP02 formal report, FP03 non-native speaker, FP07 deliberate repetition) sat in a tight cluster at 0.749–0.754, just over 0.72. The diagnosis says the real cause is upstream: both signals measure plainness, so no threshold can separate plain human writing from AI. A signal redesign is the real fix, and it's too big to make and measure as one change. Given an overlap that can't be removed, the threshold decides _who_ the errors land on. My criterion 1 says a wrong accusation costs more than a miss, so I moved the line toward fewer accusations.

**Why 0.76 and not something else.** 0.76 is the smallest round step that clears the 0.749–0.754 cluster. I'll be honest that it's fitted to the attack set: I chose it by looking at these exact scores. The "after" run on the same set will flatter it. The real test is human writing it has never seen. I didn't go to 0.85 to also clear FP05 (0.836), because that would also clear every AI piece I have except the repeated-text ones.

Commands: `python run_attacks.py --set attack_set --label after` → [results/attack_run_2026-11-11_1835_after.md](results/attack_run_2026-11-11_1835_after.md), and `python run_eval.py --label after` → [results/run_2026-11-11_1836_after.md](results/run_2026-11-11_1836_after.md).

### Attack Run — After

Every score is identical to the before run, to four decimal places, because neither signal changed. Only the label mapping moved, and exactly three attacks changed outcome:

| ID | Targeting | Before | After | Verdict before → after |
|---|---|---|---|---|
| FP02 | human writing, formal register | ai 0.752 | unsure 0.752 | BROKE → **HELD** |
| FP03 | non-native English speaker | ai 0.754 | unsure 0.754 | BROKE → **HELD** |
| FP07 | human writing repeating a phrase | ai 0.749 | unsure 0.749 | BROKE → **HELD** |
| _all other 53 attacks_ | | _same as before_ | _same as before_ | _unchanged_ |

The full 56-row table for the after run is in the results file. It matches the before table above row for row except for these three. The flood rows again came back 200 ×10 then 429 ×2.

| Family | Before: held / broke | After: held / broke |
|---|---|---|
| evasion | 1 / 9 | 1 / 9 |
| false_positive | 4 / 4 | **7 / 1** |
| prompt_injection | 3 / 3 | 3 / 3 |
| malformed | 20 / 0 | 20 / 0 |
| flood_same_creator | 12 / 0 | 12 / 0 |
| **Total** | **40 / 16** | **43 / 13** |

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 2 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. Clearly-AI vs clearly-human spread | ≥ 0.50 apart | 0.545 | 0.545 | 0.545 | MET |
| 3. All three labels reachable across 15 pieces | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeals return `under_review` and are logged | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Bad input gets a JSON response, no 500 | ≥ 8 of 10 | 10/10 | 10/10 | 10/10 | MET |

All five verdicts are the same, and all three trials were again identical. The one difference is hidden inside criterion 3. **Three of my five unedited AI pieces lost the `ai` label**: "Artificial intelligence is transforming..." (0.7454), "Remote work has become increasingly common..." (0.7232) and "Reading is one of the most valuable habits..." (0.7249) are now `unsure`. Criterion 3 still passes because three other pieces still reach `ai`. One of those three is my own plain paragraph ("I went to the store today...", 0.860), which is still a false accusation.

**Did it help, and how do I know:** It helped with the thing I aimed it at, and it cost exactly what I expected. Wrong accusations in the attack set's human family fell from **4 of 8 to 1 of 8**, including the worst outcome, FP03. The evidence is the same scores with different labels in the two results files. The cost is on the other side. Of my five genuine AI pieces, 3 are now `unsure` instead of `ai`, so I traded three caught AI pieces for three fewer accused humans, one for one. It did nothing for evasion (still 9 of 10 broke), because those were already under the old line. And the margins are thin: FP03 now clears the threshold by only 0.006. A slightly plainer version of the same writing would still be accused.

---

## What's Still Broken

| What | Stage | What I'd do | Why I stopped |
|---|---|---|---|
| **FP05** (technical docs, 0.836) and my own plain paragraph (0.860) are still called AI | Both signals | Replace the style signal's measures with ones that don't reward plainness, and add an "agreement isn't enough" rule: require some evidence beyond plainness (e.g. low perplexity _variance_ across sentences, "burstiness") before the AI label. | It's a signal redesign, not one change. Doing it alongside the threshold would make before and after impossible to compare. |
| **Evasion: 9 of 10 get through** (Pattern 1) | Signal one calibration, then label mapping | Recalibrate signal one's midpoint (perplexity 45) on a real set of AI and human text, so typical AI text scores near 0.85 instead of 0.67. | Moving it down without new signals just brings the false positives back. Patterns 1 and 3 pull the same threshold in opposite directions. |
| **EV01, PI01, PI02**: odd tokens drag signal one down | Signal one | Score perplexity per sentence and use the median, not the mean over all tokens, so one weird line or a handful of typos can't drag the whole score. Also flag text with a few extremely high-perplexity sentences for a person to look at instead of trusting the average. | Same reason: it changes signal one, and I'd want it measured on its own. |
| **EV08**: 10-word AI text scores near human | Route | Raise `MIN_WORDS` (e.g. to 40) or make anything under ~60 words always `unsure`. Ten words is not enough to judge either way. | It would also refuse or neutralise FP08-style short human posts, which currently pass. I'd want to decide that trade on purpose. |
| **EV05**: heavily human-edited AI → human | Both signals | Nothing. At that level of editing the writing is substantially human, and a style detector shouldn't claim otherwise. | Deliberate. |
| **MF07**: Arabic refused as "too short" | Route (`stylometry.words` is ASCII-only) | Count words with a Unicode-aware pattern, and return an honest "we can only check English text" message instead of "send at least 5 words". | Out of scope for this unit's one change, but it's the cheapest fix on this list. |
| **Repeated text** (MF08, criterion 5's long text) → near-certain AI | Signal one (repetition is maximally predictable) | De-duplicate repeated sentences before scoring. | It's rare for a real writer, and fixing it touches the route and signal one together. |
| **Per-creator rate limit** can be dodged by making up a new `creator_id` each time | Rate limiter key | Add a second, looser per-address limit on top of the per-creator one. | Not one of the five criteria. Noted in Rate Limiting. |

No criterion is missed, so there's no criterion fix on this list. As I said in the verdicts, though, criterion 1 was easy for my writing. The tightened version, with at least 5 plainly written pieces, is the first thing I'd run next, and I expect it to miss.

**The trade I'd make if this ran for real:** I'd keep moving toward fewer wrong accusations, as this change did, even though it means more AI-written text passes as "unsure". The people who pay are honest writers who submit alongside AI users and get compared against them, and the site, whose AI label means less. That cost is spread thin across everyone. A false accusation lands entirely on one person, and it falls hardest on careful, plain, second-language writers like FP03, who are the people least able to argue with it.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
