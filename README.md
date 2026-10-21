# NextGenAI — TD1 to TD3

## Group (DIA 1 - SUB GROUP 3)

- **Course:** Next Generation AI — ESILV
- **Student kit version:** `2026-10-14`
- **Repository:** Shared group repository for TD1, TD2 and TD3
- **Group members:**
  - NORAT Faizan
  - PERKINS Luca
  - DE GENTILE Océane
  - SAAID Myriam
  - Khadraoui Oussama
  - Richard kuete
  - VERDES Adrian
  - Samson Clément
  

## Project objective

This repository documents our experiments with multiple language models, model comparison, multi-model voting, routing strategies and cost analysis.

We preserve the prompts, model outputs, reference answers, observations, limitations and unsuccessful attempts needed to understand and reproduce our work.

## Environment

- **Operating system:** Windows
- **Python:** 3.12.12
- **Virtual environment:** `.venv`
- **Initial access check:** 5/5 required models passed on 17 October 2026
- **Database and data integrity:** verified using the provided verification script

The local access-check output is saved as `ready-for-td1.txt`. This file is intentionally excluded from the public repository.

## Reproducing the environment checks

Run these commands from the student kit directory, after configuring the required API keys as environment variables:

```powershell
.\.venv\Scripts\python.exe verify-data.py
.\.venv\Scripts\python.exe check_access.py
```

Never commit API keys, passwords, `.env` files or other credentials.

## TD1 — Model comparison

**Status:** To be completed.

Planned documentation and outputs:
- Reference questions: `reference-td1.csv`
- Question set: `questions-td1.json`
- Model configuration: `modeles-autorises.json`
- Results and analyses: to be added after the experiments
- Report: `reports/td1.md`

The report will document the experimental method, observations, reference comparisons, limitations and any failed or incomplete attempts.

## TD2 — Multi-model voting and routing

**Status:** To be completed.

The report will document the voting and routing approach, tests, results, limitations and decisions.

- Report: `reports/td2.md`

## TD3 — Configuration, cost and demonstration

**Status:** To be completed.

The report will document the configuration, cost analysis, demonstration and conclusions.

- Report: `reports/td3.md`

## Decisions, limitations and open issues

We distinguish observed results from hypotheses and interpretations. Any synthetic or replayed results will be clearly labelled and separated from real model outputs.

Open questions and limitations will be documented in the relevant TD report.

## Contributions

Each member's work and responsibilities will be recorded as the project progresses.

## Security

- Never commit API keys, passwords or credentials.
- Keep local environment files and virtual environments out of version control.
- Check every file before committing it to this public repository.
