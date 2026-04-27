# semcache

Semantic response cache for LLM-style workflows: store `(query, response)` pairs keyed by embedding similarity so paraphrases can hit the same cached answer without an exact string match.

## How it works

1. **Normalize** the query text (lowercase, collapse whitespace).
2. **Embed** with a sentence model (for example `all-mpnet-base-v2` via [Sentence Transformers](https://www.sbert.net/)).
3. **Compare** the new embedding to stored entries with cosine similarity; if any score is above a threshold, return that entry’s response.
4. **Persist** rows in **SQLite** with optional TTL.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or another PEP 621–aware installer

## Install

From the repository root (the directory that contains `pyproject.toml`):

```bash
uv sync
```

For an editable install in another environment:

```bash
uv pip install -e .
```

## Project layout

| Path | Role |
|------|------|
| `src/semcache/` | Library: `Cache`, `Storage`, `EmbeddingModel`, utilities |
| `examples/smoke_test.py` | End-to-end demo with a real embedding model |
| `pyproject.toml` | Metadata and dependencies |

## Quick start

```python
from sentence_transformers import SentenceTransformer

from semcache import Cache, Storage

model = SentenceTransformer("all-mpnet-base-v2")
storage = Storage("cache.db")
cache = Cache(model, storage, threshold=0.80)

cache.save("What is Python?", "Python is a programming language.", expires_in=3600)
answer = cache.ask("Tell me about Python programming")  # may hit if similarity >= threshold
```

Run the smoke example (downloads model weights on first run):

```bash
uv run python examples/smoke_test.py
```

## Configuration

- **`threshold`**: Minimum cosine similarity (0–1) to treat a stored query as a match.
- **`expires_in`** / storage TTL: Seconds until a row expires (`Storage.save` uses this as `ttl_seconds`).

## Development

```bash
uv sync --extra dev
uv run pytest
```

