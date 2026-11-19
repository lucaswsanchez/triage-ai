# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-19

### Added

- FastAPI backend with `POST /api/triage`, `GET /api/samples`, `GET /api/kb`, `GET /api/eval` and `GET /api/health`, documented with OpenAPI at `/docs`.
- BM25 retriever (rank_bm25) over the 21 helpdesk-kb articles, chunked by section, with accent folding, light stemming and a Spanish → English IT glossary applied only to Spanish tickets.
- `LLMProvider` abstraction with an OpenAI-compatible implementation (DeepSeek `deepseek-flash` by default), JSON mode validated with Pydantic and one retry on invalid output.
- Priority computed from impact × urgency with the helpdesk-kb priority matrix.
- Versioned prompts (`prompts/v1`), few-shot examples, prompt design document and 3 prompt injection test cases.
- Demo mode without an API key, after the hourly per-IP limit, when the daily budget is spent or on provider errors.
- Cost protection: per-IP rate limit, global daily budget, input length limit and bounded `max_tokens`.
- Evaluation dataset of 50 hand-labeled tickets and `python -m eval.run` (accuracy, confusion matrices, hit rate@k, failures).
- React + Vite + TypeScript + Tailwind frontend with Triage, Evaluation and About pages.
- First full evaluation run (`deepseek-flash`, prompt v1) and precomputed demo results for the 6 sample tickets.
- Deep link `/?sample=<id>` to open and triage a sample ticket.
- GitHub Actions CI (ruff, pytest, oxlint, prettier, vitest, build), Render blueprint, Vercel config, Dockerfiles and docker-compose.

### Fixed

- The Spanish glossary rewrote English words such as "mail" (found by the evaluation): it now applies only to tickets that look Spanish.

[1.0.0]: https://github.com/lucaswsanchez/triage-ai/releases/tag/v1.0.0
