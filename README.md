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

**What it can't see:** Predictable is not the same as machine-written. Plain writing in short sentences with common words scores as AI-like. That covers second-language writers, younger writers, and anyone writing simply on purpose. My plain human test paragraph scored **0.897**, *higher* than my clearly-AI paragraph (0.862). It also misses AI text that was prompted to use rare words, and ornate human prose scores as very human whoever wrote it.

### Signal two — the style signal

**What it measures:** Three things, each scaled to 0–1 "human-ness" between a floor and a ceiling, then combined and flipped so that higher means AI:

| Measure | How it's computed | Floor → ceiling | Weight |
|---|---|---|---|
| Sentence length spread | stdev / mean of words per sentence | 0.20 → 0.70 | 0.45 |
| Vocabulary variety | unique / total words, first 150 words only | 0.55 → 0.80 | 0.30 |
| Punctuation density | commas, semicolons, colons, dashes, brackets, quotes, `?`, `!`, ellipses per 100 words (full stops excluded) | 4 → 14 | 0.25 |

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

| Input | model_score | style_score | combined | label |
|---|---|---|---|---|
| Clearly AI | 0.862 | 0.595 | 0.755 | ai |
| Clearly human | 0.310 | 0.021 | 0.194 | human |
| Plain, ordinary human writing | 0.897 | 0.805 | 0.860 | **ai (false positive)** |
| Lightly-edited AI | 0.707 | 0.639 | 0.680 | unsure |

The plain human paragraph is the important finding. Both signals score it as *more* AI-like than the real AI text, so no weighting of these two signals can fix it, and no threshold can either without also letting the clearly-AI text through. That's why the AI label tells the writer the check can be wrong about plain writing and points them to the appeal.

**A case where my two signals split, and what my rule does with it:**
> "Honestly? I have no idea what happened at the meeting. Someone yelled; someone else left. Then the projector died -- of course -- and we all just sat there, staring at the blank wall, like it owed us an explanation!"

model_score **0.595** (common words, leaning AI) vs style_score **0.183** (lumpy sentences and lots of punctuation, clearly human). The gap is 0.41, which is over 0.35, so the weighted average of 0.430 is pulled toward 0.5 and lands at **0.465 → unsure**. The model signal alone would lean AI. The rule treats the disagreement as uncertainty instead.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was written by a person. Our automated check found the kind of variety in wording and rhythm that people's writing usually has. |
| unsure | 0.35 – 0.72 | We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces. |
| high-confidence AI | 0.72 – 1.00 | Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do. |

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

| Request | Status | `error` |
|---|---|---|
| no `text` | 400 | `missing_text` |
| `text` is whitespace | 400 | `missing_text` |
| body is `[1, 2]` | 400 | `body_not_json_object` |
| `"hi there"` | 400 | `text_too_short` |
| 25,800 characters | 200 | none (scored as 10 chunks, `"chunks": 10` in the response and log) |
| 600,000 characters | 413 | `text_too_long` |
| appeal with unknown `content_id` | 404 | `unknown_content_id` |

---

## How I Used AI

<!-- TODO (Dylan): write this yourself, two real moments. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

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
