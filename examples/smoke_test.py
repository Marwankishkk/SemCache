"""Smoke test: cache hit on paraphrase, miss on unrelated query.

Run from the repository root (the directory that contains pyproject.toml):

  uv sync
  uv run python examples/smoke_test.py
"""

import tempfile
from pathlib import Path

from sentence_transformers import SentenceTransformer

from semcache.cache import Cache
from semcache.storage import Storage


def main() -> None:
    db_path = Path(tempfile.mkstemp(prefix="semcache_test_", suffix=".db")[1])
    storage = None
    try:
        model = SentenceTransformer("all-mpnet-base-v2")
        storage = Storage(str(db_path))
        cache = Cache(model, storage, threshold=0.80)

        query_a = "what is ai "
        response_a = "ai is a field where systems learn from data."
        cache.save(query_a, response_a, expires_in=3600)

        hit = cache.ask("what is artificial intelligence")
        miss = cache.ask("What is the capital of France?")

        print("Saved:", repr(query_a))
        print("Similar query hit:", repr(hit))
        print("Unrelated query (expect None):", miss)

        if hit != response_a:
            raise SystemExit(
                f"Expected cache hit for paraphrase; got {hit!r} vs {response_a!r}"
            )
        if miss is not None:
            raise SystemExit(f"Expected miss for unrelated query; got {miss!r}")

        print("OK — cache hit on similar query, miss on unrelated.")
    finally:
        if storage is not None:
            storage.close()
        db_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
