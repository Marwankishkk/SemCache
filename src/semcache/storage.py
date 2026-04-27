import json
import sqlite3
from datetime import datetime, timedelta


class Storage:
    def __init__(self, db_path="cache.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_table()
        self.create_indexes()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL UNIQUE,
            embedding TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT
        )
        """
        self.conn.execute(sql)
        self.conn.commit()

    def create_indexes(self):
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_query ON cache(query)"
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_expires_at ON cache(expires_at)"
        )
        self.conn.commit()

    def save(self, query, embedding, response, ttl_seconds=86400):
        self.cleanup_expired()
        now = datetime.utcnow()
        expires_at = None

        if ttl_seconds:
            expires_at = (
                now + timedelta(seconds=ttl_seconds)
            ).isoformat()

        sql = """
        INSERT INTO cache (
            query,
            embedding,
            response,
            created_at,
            expires_at
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(query)
        DO UPDATE SET
            embedding=excluded.embedding,
            response=excluded.response,
            created_at=excluded.created_at,
            expires_at=excluded.expires_at
        """

        self.conn.execute(
            sql,
            (
                query,
                json.dumps(embedding.tolist()),
                response,
                now.isoformat(),
                expires_at,
            ),
        )

        self.conn.commit()

    def get(self, query):
        self.cleanup_expired()
        sql = """
        SELECT *
        FROM cache
        WHERE query = ?
        LIMIT 1
        """

        row = self.conn.execute(sql, (query,)).fetchone()

        if not row:
            return None

        if self._is_expired(row["expires_at"]):
            self.delete(query)
            return None

        return self._format_row(row)

    def get_all(self):
        rows = self.conn.execute(
            "SELECT * FROM cache"
        ).fetchall()

        results = []

        for row in rows:
            if self._is_expired(row["expires_at"]):
                continue

            results.append(self._format_row(row))

        return results

    def delete(self, query):
        self.conn.execute(
            "DELETE FROM cache WHERE query = ?",
            (query,)
        )
        self.conn.commit()

    def cleanup_expired(self):
        now = datetime.utcnow().isoformat()

        self.conn.execute(
            """
            DELETE FROM cache
            WHERE expires_at IS NOT NULL
            AND expires_at < ?
            """,
            (now,)
        )

        self.conn.commit()

    def count(self):
        row = self.conn.execute(
            "SELECT COUNT(*) as total FROM cache"
        ).fetchone()

        return row["total"]

    def _is_expired(self, expires_at):
        if expires_at is None:
            return False

        return datetime.utcnow() > datetime.fromisoformat(expires_at)

    def _format_row(self, row):
        return {
            "id": row["id"],
            "query": row["query"],
            "embedding": json.loads(row["embedding"]),
            "response": row["response"],
            "created_at": row["created_at"],
            "expires_at": row["expires_at"],
        }

    def close(self):
        self.conn.close()
