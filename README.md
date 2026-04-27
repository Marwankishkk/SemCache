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

```bash
uv sync
