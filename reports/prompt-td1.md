# TD 1 prompt (verbatim)

Source: `skeleton-multi-llm-en.py` from the student kit (pack 2026-10-14), constants `SYSTEM_PROMPT` and `USER_PROMPT_TEMPLATE`, **used unchanged** and identical for the five models.

`{schema}` is replaced by the content of `schema.sql` (stripped) and `{question}` by the question text from `questions-td1.json`. The trace column `prompt_sha256` is `sha256(SYSTEM_PROMPT + "\n" + user_message)`.

**Check:** recomputing this hash from the unmodified skeleton and `schema.sql` gives exactly the `prompt_sha256` recorded in `data/traces/traces-td1.csv` for all 20 questions (20/20), so every model received this exact prompt.

## System message

```text
You write SQLite queries for a small e-commerce database. Reply with exactly one SQLite SELECT statement and nothing else: no explanation, no comments, no markdown other than an optional ```sql fence.
```

## User message template

```text
Schema (SQLite):
{schema}

Conventions (binding):
- product.price is the unit price in euro cents, excluding VAT (an integer). Revenue excluding VAT is SUM(quantity_product * price), an integer number of cents.
- orders holds order lines: one row per (order_id, product_id). All lines of an order share the same customer_id and the same date.
- orders.date and customers.insert_date are UTC timestamps stored as text 'YYYY-MM-DD HH:MM:SS'. customers.birth_date is a date stored as text 'YYYY-MM-DD'. Compare them as text or with SQLite date functions.
- A period "from S to E" is closed on the left and open on the right: date >= S AND date < E.
- A customer's age on a day D is the number of completed years: someone born on B is N years old on D when the N-th anniversary of B is on or before D and the (N+1)-th anniversary is after D. "Exactly 25 years old" means completed age 25 on that day, computed from month and day, never from the year difference alone.
- Unless the question says "at the time of the order", ages are computed on the reference date given in the question.
- The query must return exactly one row and one column named revenue_cents. When no order line matches, return 0 (use COALESCE), not NULL.
- Use only the tables above. One SELECT statement, nothing else.

Question: {question}
```

## Call parameters (from `modeles-autorises.json`)

| Model | Provider | Parameters |
|---|---|---|
| `openai/gpt-oss-120b` | Groq | temperature 0, `reasoning_effort` low, `max_completion_tokens` 1024 |
| `openai/gpt-oss-20b` | Groq | temperature 0, `reasoning_effort` low, `max_completion_tokens` 1024 |
| `cohere/north-mini-code:free` | OpenRouter | temperature 0, `reasoning` disabled, `max_tokens` 1024, `max_price` 0 |
| `qwen/qwen3.8-27b` | Groq | temperature 0, `reasoning_effort` none, `max_completion_tokens` 1000 |
| `dots-studio/dots-3-note-preview:free` | OpenRouter | temperature 0, `reasoning` disabled, `max_tokens` 1024, `max_price` 0 |
