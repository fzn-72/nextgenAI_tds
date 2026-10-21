# TD 1 report — Five free models write SQL, measured against our own reference

Session: 21 October 2026. Kit: pack 2026-10-14. All rows in this report are **real** calls (`nature = real`); no replayed or simulated row is used.

## 1. What we did

| Step | Status | Evidence |
|---|---|---|
| Reference: 20 SQLite queries, executed and independently checked | Done, 20/20 | [`data/references/reference-td1.csv`](../data/references/reference-td1.csv), [`scripts/check_references.py`](../scripts/check_references.py), [`outputs/checks/check_references_output.txt`](../outputs/checks/check_references_output.txt) |
| Batch: 20 questions x 5 models = 100 cells | Done, 100/100 cells executed | [`data/traces/`](../data/traces/), [`data/states/`](../data/states/) |
| Merged trace table, one line per HTTP attempt | Done, 106 lines | [`data/traces/traces-td1.csv`](../data/traces/traces-td1.csv) |
| Long comparison, one final row per model/question | Done, 100 rows | [`analysis/csv/model-question-comparison-en.csv`](../analysis/csv/model-question-comparison-en.csv) |
| Models x questions matrix (pivot of the CSV above) | Done | [`analysis/spreadsheets/matrix-td1.xlsx`](../analysis/spreadsheets/matrix-td1.xlsx) |
| Five-model summary | Done | [`analysis/csv/five-model-summary-en.csv`](../analysis/csv/five-model-summary-en.csv) |
| Prompt, verbatim | Done, unchanged skeleton prompt | [`prompt-td1.md`](prompt-td1.md) |

### Reference and independent check

Each reference query follows the conventions of the protocol: period closed on the left and open on the right (`date >= S AND date < E`), completed age computed from month and day, revenue `SUM(quantity_product * price)` in cents excluding VAT, `COALESCE(..., 0)` when nothing matches.

Independent check: `scripts/check_references.py` recomputes the 20 amounts **in plain Python from the CSV files, without SQL**, and also re-executes each reference query on the read-only database. The three values (CSV file, SQL, Python) agree for 20/20 questions.

Boundary cases worth noting: C05 includes order O0105 placed exactly at `2026-06-01 00:00:00` (left bound closed); C07 includes O0104 at `2026-05-31 23:59:59` and excludes O0105 (right bound open); C06 and C14 match no order line, hence 0 and not NULL.

### Calls

- 100 initial calls: 60 Groq (A, B, D) and 40 OpenRouter (C, E), plus **6 retries**, all after HTTP 429: 1 for gpt-oss-20b (C19, tokens-per-minute limit 8000) and 5 for qwen3.8-27b (C16 to C20, output-tokens-per-minute limit 1000). Every retry is kept as its own trace line; the last attempt gives the verdict.
- No access failure (no 400-404), no timeout, no truncation.
- Same prompt fingerprint on every line of a question: recomputed from the unmodified skeleton, 20/20 match.

## 2. Results

Final verdict = last attempt of each cell. Codes: OK correct, X wrong value, SQL syntax error (`sql_invalid`), FMT rejected by the sandbox (`sql_rejected`).

| Model | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | C15 | C16 | C17 | C18 | C19 | C20 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-oss-120b (Groq) | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | X | OK | **19/20** |
| gpt-oss-20b (Groq) | OK | X | OK | OK | OK | OK | OK | OK | OK | OK | X | OK | OK | OK | OK | OK | OK | OK | OK | OK | **18/20** |
| cohere north-mini-code (OpenRouter) | OK | SQL | OK | OK | OK | OK | OK | X | X | X | X | OK | OK | OK | X | OK | X | OK | OK | OK | **13/20** |
| qwen3.8-27b (Groq) | OK | OK | OK | OK | OK | OK | OK | OK | OK | X | OK | FMT | OK | OK | X | OK | X | OK | X | OK | **15/20** |
| dots-3-note-preview (OpenRouter) | OK | X | OK | OK | OK | OK | OK | X | OK | X | OK | OK | OK | OK | X | OK | SQL | OK | OK | OK | **15/20** |

By family (details in the five-model summary):

| Family | Questions | Correct cells |
|---|---|---|
| Period | C01, C04, C05, C06, C07, C20 | 30/30 |
| Product list | C03, C12, C13, C14 | 19/20 |
| Age (reference date or at order) | C02, C08, C09, C10, C11 | 14/25 |
| Combined filters | C15 to C19 | 17/25 |

Median latency of successful calls: Groq 0.5 to 0.8 s, OpenRouter free routes 2.4 to 2.8 s. Groq returns no native cost (empty, not zero); OpenRouter returns `cost_native = 0` on the `:free` routes.

## 3. Failures and observed causes

The SQL text and the error fields of each failure are explained row by row in `model-question-comparison-en.csv`. Summary:

- **20 failed cells: 17 wrong values, all on questions with an age filter**, plus 2 syntax errors and 1 format failure. Typical patterns: year difference only, without the month-day correction (C10, C15); wrong birth-date window (gpt-oss-20b C02: born in the last year, i.e. age 0; C11: ages 20 to 24); equality on one birth date instead of a one-year window (gpt-oss-120b C19); contradictory month-day conditions that select nobody and return 0 (several C08, C09, C15 cells); off-by-one on the anniversary day (qwen C17).
- **Two SQL syntax errors** (`sql_invalid`): Cohere C02 and Dots C17, both `syntax error near "AS"` (alias inside WHERE, misplaced parenthesis in CAST).
- **One output-format failure** (`sql_rejected`): qwen C12 opens a ```` ```sql ```` fence and never closes it; the skeleton only strips a complete fence, so the sandbox rejects the text as not a SELECT. The SQL inside was never executed: this is a format failure, not a logic error.
- **No access failure.** The six HTTP 429 were temporary rate-limit errors, each followed by one retry within the protocol.

**Wrong consensus observed (input for TD 2):** on C10 (age at the time of the order) Cohere, Qwen and Dots all return **119410** instead of 558980. All three keep only "year difference = 25 and birthday already passed" and miss "year difference = 26 and birthday not yet passed" (439570 cents). A 3-of-5 vote would accept a wrong value here.

## 4. Limitations

- One run per cell at temperature 0, 20 questions: the scores support a routing hypothesis for this batch, not a general ranking or error rate.
- The 429 retries depend on our accounts' per-minute limits on 21 October 2026; another account or time may differ.
- Public index and prices come from the kit (portfolio snapshot of 28 Sep 2026, Groq prices of 5 Oct 2026). Cohere north-mini-code and Dots-3-note have no documented index nor paid route of the exact same model: N/A.
- Real spend is 0 on the free plans/routes used; Groq's empty `cost_native` is recorded as missing, not as zero.

## 5. Contributions

| Member | Role in TD 1 | Work |
|---|---|---|
| VERDES Adrian | A | Batch gpt-oss-120b (Groq), `traces-A.csv` |
| PERKINS Luca | B | Batch gpt-oss-20b (Groq), `traces-B.csv`, `comparison-B.csv` |
| KUETE Richard | C | Batch cohere north-mini-code (OpenRouter), `traces-C.csv` |
| KHADRAOUI Oussama | D | Batch qwen3.8-27b (Groq), `traces-D.csv` |
| DE GENTILE Océane | E | Batch dots-3-note-preview (OpenRouter), `traces-E.csv` |
| SAMSOM Clément | F | [to complete] |
| SAAID Myriam | G | References C05-C07; independent cross-check of the 20 references (`check_references.py`); trace merge audit; `model-question-comparison-en.csv` and `five-model-summary-en.csv`; prompt file |
| NORAT Faizan | H | [to complete] |

All members wrote and cross-checked two or three reference queries. Coding assistance (Claude) was used for the cross-check script and the summary CSVs; the code was run and verified by the group, and no reference amount comes from a model answer.

## 6. Next steps (TD 2)

- Run the k-of-n vote on the saved traces (no new calls); use C10 as the wrong-consensus case.
- Routing hypothesis to test: period and product questions are solved by every model; age and combined questions should go to gpt-oss-120b / gpt-oss-20b first, with disagreement reported instead of a value.
- Person preparing TD 2 (reading `atelier-vote.py`): [name].
