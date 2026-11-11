# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 18:35
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `856a0810-6903-4c46-be03-9d4b8ab2fa50` | unsure | 0.439 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1319f45f-5c92-44d6-b575-b1a1cfa31e43` | unsure | 0.457 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `1bb30fab-fcac-458b-8daa-ff3117c08850` | unsure | 0.566 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a3a6cb67-879c-483f-b9bc-2d06ae92e618` | unsure | 0.647 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `85a02680-2d28-45f5-9942-d3b37e7ac678` | human | 0.296 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `1e11bd15-c398-474b-91c1-adb42c90d18b` | unsure | 0.468 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `9aa59b53-69fb-4b17-a955-7e145ab8da5d` | unsure | 0.545 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `0e2f5978-2c98-4889-bc7d-676740447065` | unsure | 0.355 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `dabfd246-4db1-4091-b165-98d1e63e8531` | unsure | 0.601 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `b11e66dd-1ad0-4f14-ba4d-fa821f934900` | ai | 0.918 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `d6185a59-64cf-47e4-bc26-752b5d3111be` | unsure | 0.602 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `d7ba75ef-807c-4a1a-9a76-60fffa239240` | unsure | 0.752 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `d87748ef-1ba4-4bee-a32b-2afbcf1cee27` | unsure | 0.754 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e11bb9ea-7bf0-434b-8dc5-0bec277fc4a3` | unsure | 0.720 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `bf3eea39-7601-4b92-b550-290a672826a3` | ai | 0.836 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c95714d0-dd64-4641-baba-af6a68117c69` | unsure | 0.613 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `1d7a2c4c-7eec-4f45-8797-e0955eb223f8` | unsure | 0.749 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `abfa39be-e10a-4aea-9f9a-16e124bf7177` | unsure | 0.393 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `fed7cb27-3669-4908-be89-0aa4b98607c2` | unsure | 0.413 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ba6c995b-6dd2-4a5b-8bb2-9eeb7caffd61` | human | 0.257 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8db10bec-19f1-44a3-a3fe-0583d5d123f9` | unsure | 0.569 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `25959885-d8df-448f-84b1-4e2ec081ee3e` | unsure | 0.475 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c6d03a09-9c4f-4d2a-8e37-2ac9b7ab5ce4` | unsure | 0.525 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c03094e6-dafd-46e9-a5d0-e673c1f4f568` | unsure | 0.571 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 200 | `a4806898-07d6-401e-b08a-1f95bb12ab9c` | ai | 0.904 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4ec73693-9be0-43c2-b1c7-416bf26f40fa` | unsure | 0.365 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7cf269d4-79af-4cb6-9ea4-9d84fda3345a` | unsure | 0.365 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ceb73866-2351-4704-9de2-334b27b6609d` | unsure | 0.365 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fec5907c-995a-4d51-85b0-ce012ab81857` | unsure | 0.365 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `be5b8319-fa24-422c-a52c-2ff544b54074` | unsure | 0.365 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1c9d9aba-6e82-4d53-b7c3-d68e14a938b2` | unsure | 0.365 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9b10228f-d49f-4559-b4cb-212af0e62b45` | unsure | 0.365 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `22944529-7da5-4279-b255-99162e553ee2` | unsure | 0.365 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a8e53e44-8bc0-4b9f-b851-ec3c8741864a` | unsure | 0.365 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `60b65f64-c624-44e0-8348-c4a35ef50a20` | unsure | 0.365 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "856a0810-6903-4c46-be03-9d4b8ab2fa50",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.439,
  "model_score": 0.1635,
  "style_score": 0.7,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "1319f45f-5c92-44d6-b575-b1a1cfa31e43",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4566,
  "model_score": 0.5943,
  "style_score": 0.25,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "1bb30fab-fcac-458b-8daa-ff3117c08850",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.566,
  "model_score": 0.6662,
  "style_score": 0.4158,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "a3a6cb67-879c-483f-b9bc-2d06ae92e618",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6468,
  "model_score": 0.6114,
  "style_score": 0.7,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "85a02680-2d28-45f5-9942-d3b37e7ac678",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2958,
  "model_score": 0.3212,
  "style_score": 0.2578,
  "label": "We think this was written by a person. Our automated check found the kind of variety in wording and rhythm that people's writing usually has.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "1e11bd15-c398-474b-91c1-adb42c90d18b",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4676,
  "model_score": 0.5727,
  "style_score": 0.31,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "9aa59b53-69fb-4b17-a955-7e145ab8da5d",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5446,
  "model_score": 0.5862,
  "style_score": 0.4822,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "0e2f5978-2c98-4889-bc7d-676740447065",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3555,
  "model_score": 0.2452,
  "style_score": 0.5209,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "dabfd246-4db1-4091-b165-98d1e63e8531",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6012,
  "model_score": 0.7042,
  "style_score": 0.4466,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "b11e66dd-1ad0-4f14-ba4d-fa821f934900",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9177,
  "model_score": 0.9792,
  "style_score": 0.8255,
  "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "d6185a59-64cf-47e4-bc26-752b5d3111be",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6016,
  "model_score": 0.6175,
  "style_score": 0.5778,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "d7ba75ef-807c-4a1a-9a76-60fffa239240",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7517,
  "model_score": 0.7387,
  "style_score": 0.7711,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "d87748ef-1ba4-4bee-a32b-2afbcf1cee27",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7539,
  "model_score": 0.8051,
  "style_score": 0.6771,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "e11bb9ea-7bf0-434b-8dc5-0bec277fc4a3",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7197,
  "model_score": 0.8329,
  "style_score": 0.55,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "bf3eea39-7601-4b92-b550-290a672826a3",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8355,
  "model_score": 0.8005,
  "style_score": 0.888,
  "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c95714d0-dd64-4641-baba-af6a68117c69",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6127,
  "model_score": 0.8814,
  "style_score": 0.4914,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "1d7a2c4c-7eec-4f45-8797-e0955eb223f8",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7486,
  "model_score": 0.8816,
  "style_score": 0.5492,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "abfa39be-e10a-4aea-9f9a-16e124bf7177",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3929,
  "model_score": 0.3223,
  "style_score": 0.4987,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "fed7cb27-3669-4908-be89-0aa4b98607c2",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4126,
  "model_score": 0.4625,
  "style_score": 0.3377,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "ba6c995b-6dd2-4a5b-8bb2-9eeb7caffd61",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2573,
  "model_score": 0.2044,
  "style_score": 0.3367,
  "label": "We think this was written by a person. Our automated check found the kind of variety in wording and rhythm that people's writing usually has.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "8db10bec-19f1-44a3-a3fe-0583d5d123f9",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5693,
  "model_score": 0.5943,
  "style_score": 0.5319,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "25959885-d8df-448f-84b1-4e2ec081ee3e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.475,
  "model_score": 0.4998,
  "style_score": 0.4379,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c6d03a09-9c4f-4d2a-8e37-2ac9b7ab5ce4",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5252,
  "model_score": 0.6401,
  "style_score": 0.3529,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c03094e6-dafd-46e9-a5d0-e673c1f4f568",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5708,
  "model_score": 0.5583,
  "style_score": 0.5895,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "a4806898-07d6-401e-b08a-1f95bb12ab9c",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.9036,
  "model_score": 0.9878,
  "style_score": 0.7772,
  "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "4ec73693-9be0-43c2-b1c7-416bf26f40fa",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "7cf269d4-79af-4cb6-9ea4-9d84fda3345a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "ceb73866-2351-4704-9de2-334b27b6609d",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "fec5907c-995a-4d51-85b0-ce012ab81857",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "be5b8319-fa24-422c-a52c-2ff544b54074",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "1c9d9aba-6e82-4d53-b7c3-d68e14a938b2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "9b10228f-d49f-4559-b4cb-212af0e62b45",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "22944529-7da5-4279-b255-99162e553ee2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "a8e53e44-8bc0-4b9f-b851-ec3c8741864a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "60b65f64-c624-44e0-8348-c4a35ef50a20",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.3646,
  "model_score": 0.0287,
  "style_score": 0.53,
  "label": "We couldn't tell whether this was written by a person or with help from an AI tool, so we aren't making a call either way. This isn't an accusation, and nothing about how your work is shown has changed. Automated checks are often unsure about short or plainly written pieces.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
