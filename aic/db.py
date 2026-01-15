import sqlite3
import os

DB_PATH = ".aic/graph.db"

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                path TEXT PRIMARY KEY,
                hash TEXT,
                skeleton TEXT,
                status TEXT DEFAULT 'CLEAN'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                source TEXT,
                target TEXT,
                PRIMARY KEY (source, target),
                FOREIGN KEY(source) REFERENCES nodes(path)
            )
        """)

def upsert_node(path, hash_val, skeleton):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO nodes (path, hash, skeleton, status)
            VALUES (?, ?, ?, 'CLEAN')
            ON CONFLICT(path) DO UPDATE SET
                hash = excluded.hash,
                skeleton = excluded.skeleton,
                status = 'CLEAN'
        """, (path, hash_val, skeleton))

def mark_dirty(path):
    """Mark all nodes that depend on this path as DIRTY."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE nodes
            SET status = 'DIRTY'
            WHERE path IN (
                SELECT source FROM edges WHERE target = ?
            )
        """, (path,))

def update_edges(source_path, target_paths):
    with get_connection() as conn:
        conn.execute("DELETE FROM edges WHERE source = ?", (source_path,))
        for target in target_paths:
            conn.execute("INSERT OR IGNORE INTO edges (source, target) VALUES (?, ?)", (source_path, target))

def get_node(path):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM nodes WHERE path = ?", (path,)).fetchone()

def get_dependencies(path):
    with get_connection() as conn:
        return [row['target'] for row in conn.execute("SELECT target FROM edges WHERE source = ?", (path,)).fetchall()]
