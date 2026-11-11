# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 18:08
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `476517a3-ae4e-4368-ab5d-d54e5784cfa2` | unsure | 0.439 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `feb4aa06-f009-4570-80ea-27fc23b44725` | unsure | 0.457 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `0794dcc9-09d8-44bc-b52b-a95623b4e0a8` | unsure | 0.566 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c49bcebe-5770-4b3c-9155-e5c25d3f4d56` | unsure | 0.647 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `71852210-083c-4f75-bba3-e09e25fc8a24` | human | 0.296 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `fc872dde-9f1c-43bc-b726-159fc67db274` | unsure | 0.468 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `96682e9c-467a-45c0-9f9b-4a554ade91de` | unsure | 0.545 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `481a9dc9-d1e3-4c13-b87d-4277d73c27d8` | unsure | 0.355 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f1a0cba0-5765-4cc9-ab33-2e99b431f04b` | unsure | 0.601 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `1db939b6-fdfd-4a21-9726-08fbff1aaed6` | ai | 0.918 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `4db6e660-0437-4584-8c32-3ebce237ade4` | unsure | 0.602 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `7e29aa06-2887-4745-870e-96863dc6a8f7` | ai | 0.752 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `44a080f5-9dcb-4900-aa59-c33bdc91afca` | ai | 0.754 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `64fca975-db7f-407f-9111-40a2365840a4` | unsure | 0.720 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `44f97bb2-9fe4-47ea-8165-ae612072b6e1` | ai | 0.836 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `f2b07295-f2ac-4a58-8a1b-34d449ff86df` | unsure | 0.613 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `edb46fa8-7403-450d-9f63-43ccc2e95ab5` | ai | 0.749 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `7ea56f93-9303-4a8d-a336-144cf14149bb` | unsure | 0.393 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `34845d8b-cec8-4dcb-af9a-2a98a45567a5` | unsure | 0.413 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ca25d96f-4b32-4b42-b800-28876ededd15` | human | 0.257 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `16191511-d4e8-45cc-9596-181cbecd0fca` | unsure | 0.569 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `84714129-dd52-4c4e-94e6-76a00ac76d84` | unsure | 0.475 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `2582c178-dc37-4053-8a8c-9b70e5409d33` | unsure | 0.525 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `f8e4b82d-c58a-478b-b9b8-b866a0b8c68d` | unsure | 0.571 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 200 | `10b84bf5-54c1-4d70-90a0-0ecf7ce4dd4a` | ai | 0.904 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d57086cb-3fbf-411c-b93d-dc52d3a8d69f` | unsure | 0.365 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `da392e82-c369-4974-8eb1-46ee76f3bd3b` | unsure | 0.365 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1f0e9a57-e4e8-4420-b556-06e45e21ac59` | unsure | 0.365 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9691338f-8bbc-4ffe-b847-2367cd888c75` | unsure | 0.365 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9572d826-45f6-4a8e-bb82-7995b65e9e2e` | unsure | 0.365 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2d9d27b9-92ae-4356-bde6-7e2a534a3200` | unsure | 0.365 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `726cd4a1-9ccf-4412-965a-86e9d346e890` | unsure | 0.365 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `93b99d30-4c3c-40b3-b6d4-9791d8729881` | unsure | 0.365 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b1e5aa6a-ec3a-4376-8da3-6d0162c70e7f` | unsure | 0.365 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4d0470f3-f8e5-48bb-875a-048c40cb92ef` | unsure | 0.365 |  |
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
  "content_id": "476517a3-ae4e-4368-ab5d-d54e5784cfa2",
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
  "content_id": "feb4aa06-f009-4570-80ea-27fc23b44725",
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
  "content_id": "0794dcc9-09d8-44bc-b52b-a95623b4e0a8",
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
  "content_id": "c49bcebe-5770-4b3c-9155-e5c25d3f4d56",
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
  "content_id": "71852210-083c-4f75-bba3-e09e25fc8a24",
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
  "content_id": "fc872dde-9f1c-43bc-b726-159fc67db274",
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
  "content_id": "96682e9c-467a-45c0-9f9b-4a554ade91de",
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
  "content_id": "481a9dc9-d1e3-4c13-b87d-4277d73c27d8",
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
  "content_id": "f1a0cba0-5765-4cc9-ab33-2e99b431f04b",
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
  "content_id": "1db939b6-fdfd-4a21-9726-08fbff1aaed6",
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
  "content_id": "4db6e660-0437-4584-8c32-3ebce237ade4",
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
  "content_id": "7e29aa06-2887-4745-870e-96863dc6a8f7",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7517,
  "model_score": 0.7387,
  "style_score": 0.7711,
  "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
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
  "content_id": "44a080f5-9dcb-4900-aa59-c33bdc91afca",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7539,
  "model_score": 0.8051,
  "style_score": 0.6771,
  "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
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
  "content_id": "64fca975-db7f-407f-9111-40a2365840a4",
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
  "content_id": "44f97bb2-9fe4-47ea-8165-ae612072b6e1",
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
  "content_id": "f2b07295-f2ac-4a58-8a1b-34d449ff86df",
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
  "content_id": "edb46fa8-7403-450d-9f63-43ccc2e95ab5",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7486,
  "model_score": 0.8816,
  "style_score": 0.5492,
  "label": "Our automated check thinks this may have been written with help from an AI tool. Checks like this can be wrong, especially about plain or simple writing. If you wrote this yourself, you can ask for a person to review it, and we'll mark it as under review while they do.",
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
  "content_id": "7ea56f93-9303-4a8d-a336-144cf14149bb",
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
  "content_id": "34845d8b-cec8-4dcb-af9a-2a98a45567a5",
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
  "content_id": "ca25d96f-4b32-4b42-b800-28876ededd15",
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
  "content_id": "16191511-d4e8-45cc-9596-181cbecd0fca",
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
  "content_id": "84714129-dd52-4c4e-94e6-76a00ac76d84",
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
  "content_id": "2582c178-dc37-4053-8a8c-9b70e5409d33",
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
  "content_id": "f8e4b82d-c58a-478b-b9b8-b866a0b8c68d",
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
  "content_id": "10b84bf5-54c1-4d70-90a0-0ecf7ce4dd4a",
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
  "content_id": "d57086cb-3fbf-411c-b93d-dc52d3a8d69f",
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
  "content_id": "da392e82-c369-4974-8eb1-46ee76f3bd3b",
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
  "content_id": "1f0e9a57-e4e8-4420-b556-06e45e21ac59",
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
  "content_id": "9691338f-8bbc-4ffe-b847-2367cd888c75",
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
  "content_id": "9572d826-45f6-4a8e-bb82-7995b65e9e2e",
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
  "content_id": "2d9d27b9-92ae-4356-bde6-7e2a534a3200",
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
  "content_id": "726cd4a1-9ccf-4412-965a-86e9d346e890",
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
  "content_id": "93b99d30-4c3c-40b3-b6d4-9791d8729881",
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
  "content_id": "b1e5aa6a-ec3a-4376-8da3-6d0162c70e7f",
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
  "content_id": "4d0470f3-f8e5-48bb-875a-048c40cb92ef",
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
