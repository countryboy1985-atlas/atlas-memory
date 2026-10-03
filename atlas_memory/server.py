import asyncio
import sqlite3
import os

from mcp.server.fastmcp import FastMCP

DB_DIR = "/data"
DB = os.path.join(DB_DIR, "atlas.db")

mcp = FastMCP("Atlas Memory", host="0.0.0.0", port=8765)


def connect_db():
    os.makedirs(DB_DIR, exist_ok=True)
    db = sqlite3.connect(DB)
    db.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    return db


@mcp.tool()
def remember(content: str, category: str = "general") -> str:
    """Save useful information to Atlas's persistent memory."""
    content = content.strip()
    category = category.strip() or "general"

    if not content:
        return "Nothing was provided to remember."

    db = connect_db()
    cursor = db.execute(
        "INSERT INTO memories (category, content) VALUES (?, ?)",
        (category, content),
    )
    db.commit()
    memory_id = cursor.lastrowid
    db.close()

    return f"Memory {memory_id} saved."


@mcp.tool()
def recall(query: str, limit: int = 10) -> str:
    """Search Atlas's persistent memories for relevant information."""
    query = query.strip()

    if not query:
        return "A search query is required."

    limit = max(1, min(limit, 20))

    db = connect_db()
    rows = db.execute(
        """
        SELECT id, category, content, created_at
        FROM memories
        WHERE content LIKE ? OR category LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (f"%{query}%", f"%{query}%", limit),
    ).fetchall()
    db.close()

    if not rows:
        return "No matching memories found."

    return "\n".join(
        f"[{row[0]}] ({row[1]}) {row[2]} — {row[3]}"
        for row in rows
    )


if __name__ == "__main__":
    connect_db().close()
    mcp.run(transport="sse")
