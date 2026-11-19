# Evaluation

`dataset.jsonl` has **50 tickets written and labeled by hand** for this project (37 in English, 13 in Spanish). Each row has:

| Field | Meaning |
|---|---|
| `category` | Expected category (the 7 KB categories plus `Other` for out-of-scope requests). |
| `impact`, `urgency` | Expected values, following the helpdesk-kb priority matrix. |
| `priority` | P1–P4, derived from impact × urgency with the same matrix the app uses. |
| `level` | Expected support level (L1/L2). |
| `article` | The KB article that solves the ticket (`null` for the 4 out-of-scope tickets). |

Distribution: 8 Accounts & Identity, 8 Microsoft 365, 8 Hardware & Printing, 7 Network, 6 Security, 5 Software, 4 Onboarding & Offboarding, 4 Other. Priorities: 1 P1, 9 P2, 14 P3, 26 P4 (the skew towards P3/P4 is realistic for a service desk).

## Running it

```bash
cd backend
python -m eval.run --retrieval-only   # no API key needed
python -m eval.run                    # full run, needs LLM_API_KEY (about 53 LLM calls)
```

The script writes `results.json`, which the API serves at `GET /api/eval` and the frontend shows on the Evaluation page.

## Metrics

- **Retrieval**: hit rate@1 and @3 (is the labeled article among the top results?) and MRR@3, per language. Also an ablation without the Spanish glossary.
- **Retrieval baseline classifier**: the category of the top BM25 article. It shows how much the LLM adds over a pure search.
- **Classification** (full run only): category accuracy, priority accuracy (exact and within one level), level and language accuracy, citation accuracy (did the model cite the labeled article?), confusion matrices for category and priority, failed examples, latency and tokens.
- **Prompt injection cases**: the 3 cases in `prompts/injection_cases.jsonl`, checked against their expectations.

## Honest caveats

- **Small, self-written dataset.** 50 tickets written by the same person who wrote the prompt and the glossary. They are realistic but cleaner than real tickets (no signatures, threads or typos-heavy text). Treat the numbers as a sanity check, not a benchmark.
- **The dataset is no longer a pure hold-out set.** The first retrieval run (hit@3 = 0.978, 45/46) missed T42: the English phrase "mail it back" was rewritten to "email" by the Spanish glossary, which pulled up the Outlook article. The fix (apply the glossary only to tickets that look Spanish, never to the English KB) is a real bug fix, but it was found with this dataset. After it: hit@3 = 1.0, hit@1 dropped from 0.935 to 0.913.
- **Priority labels are judgement calls.** Impact and urgency are partly subjective; "priority within one level" is reported for that reason.
- **LLM results vary** slightly between runs even at temperature 0.2. Each run is stored with its date, model and prompt version.
