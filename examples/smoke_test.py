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

        # --- Seed the cache with multiple entries ---
        entries = [
            (
                "what is ai",
                "AI is a field where systems learn from data.",
            ),
            (
                "how does Python work",
                "Python is an interpreted high-level programming language.",
            ),
            (
                "what is climate change",
                "Climate change refers to long-term shifts in global temperatures and weather patterns.",
            ),
            (
                "explain the internet",
                "The internet is a global network of interconnected computers that communicate via standardised protocols.",
            ),
        ]
        for query, response in entries:
            cache.save(query, response, expires_in=3600)
            print(f"Saved: {query!r}")

        print()

        # --- Hit cases (paraphrases of saved queries) ---
        hit_cases = [
            ("what is artificial intelligence",       entries[0][1]),
            ("define AI",                             entries[0][1]),
            ("how does the Python language work",     entries[1][1]),
            ("what is global warming",                entries[2][1]),
            ("how does the web work",                 entries[3][1]),
        ]

        # --- Miss cases (unrelated queries) ---
        miss_cases = [
            "What is the capital of France?",
            "Who wrote Hamlet?",
            "What is the boiling point of water?",
            "How do I bake sourdough bread?",
            "What is the speed of light?",
        ]

        # --- Run hit assertions ---
        print("=== Hit cases ===")
        for ask_query, expected_response in hit_cases:
            result = cache.ask(ask_query)
            print(f"  ask:      {ask_query!r}")
            print(f"  response: {result!r}")
            if result != expected_response:
                raise SystemExit(
                    f"Expected cache hit for {ask_query!r}; "
                    f"got {result!r} vs {expected_response!r}"
                )
            print("  -> HIT OK")
            print()

        # --- Run miss assertions ---
        print("=== Miss cases ===")
        for ask_query in miss_cases:
            result = cache.ask(ask_query)
            print(f"  ask:      {ask_query!r}")
            print(f"  response: {result!r}")
            if result is not None:
                raise SystemExit(
                    f"Expected miss for {ask_query!r}; got {result!r}"
                )
            print("  -> MISS OK")
            print()

        print("OK — all hit and miss assertions passed.")

    finally:
        if storage is not None:
            storage.close()
        db_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()