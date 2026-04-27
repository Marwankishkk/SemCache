# SemCache

A simple semantic cache for LLM apps.

It stores `(query → response)` pairs and uses embeddings to return cached answers for similar questions (not exact matches).

---

## How it works

1. Clean the input query (lowercase + normalize spaces)
2. Convert it into an embedding
3. Compare it with stored embeddings using cosine similarity
4. If similarity is high enough → return cached response
5. Otherwise → treat as a new query and store it

---

## Why this matters

Instead of calling an LLM every time, you reuse previous answers for similar questions.

This saves:
- API cost
- latency
- compute

---

## Tech stack

- Python 3.12+
- Sentence Transformers
- SQLite
- NumPy

---

## Install

From the project root (the directory that contains `pyproject.toml`):

```bash
uv sync
```

---

## How to run

**Smoke example** (downloads the embedding model on first run, then exercises cache hit/miss):

```bash
uv run python examples/smoke_test.py
```

**Tests** (install dev dependencies first):

```bash
uv sync --extra dev
uv run pytest
```

Use `semcache` as a library in your own Python code after `uv sync`; import `Cache`, `EmbeddingModel`, and `Storage` from `semcache` (see `examples/smoke_test.py`).
