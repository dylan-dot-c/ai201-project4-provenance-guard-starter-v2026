# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives on my own writing

Of 10 pieces I wrote myself, at most 2 are labelled high-confidence AI.

**Why this target:** A wrong accusation costs a real writer much more than a missed AI piece costs the site. I allow 2 rather than 0 because plain writing with common vocabulary reads as AI-like to both signals, and I've already seen that happen.

---

## 2. Score spread between clearly-AI and clearly-human text

The clearly-AI calibration piece and the clearly-human calibration piece (both quoted in the README) score at least 0.5 apart on the combined confidence score.

**Why this target:** The system has to be sure something isn't AI before it says so, so clearly-AI and clearly-human writing should be strongly separated, not just slightly apart.

---

## 3. Every label is reachable

Across a test set of 15 pieces, each of the three labels (high-confidence human, unsure, high-confidence AI) is returned at least once.

**Why this target:** <!-- TODO (Dylan): your reason -->

---

## 4. The appeal path

Of 10 appeals sent with a real content_id, all 10 return status `under_review` and appear in `logs/audit.jsonl` next to the original decision.

**Why this target:** <!-- TODO (Dylan): your reason -->

---

## 5. Bad input

Of 10 bad-input test cases (missing text, empty text, text over 20,000 characters, a body that isn't JSON, and similar), at least 8 get a JSON response instead of a crash (no 500). Text over the length limit is split into chunks and scored rather than rejected outright.

**Why this target:** A long piece of writing is still real writing, so it should get scored rather than turned away with an error. <!-- TODO (Dylan): check this says what you meant -->

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
