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

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |         |
| 2.        |        |       |       |       |         |
| 3.        |        |       |       |       |         |
| 4.        |        |       |       |       |         |
| 5.        |        |       |       |       |         |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

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
