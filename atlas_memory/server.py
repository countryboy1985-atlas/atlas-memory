from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_DIR = "/data"
DB = os.path.join(DB_DIR, "atlas.db")


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


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Atlas Memory"
    })


@app.post("/remember")
def remember():
    data = request.get_json(silent=True) or {}

    category = data.get("category", "general")
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "content is required"}), 400

    db = connect_db()
    cursor = db.execute(
        "INSERT INTO memories (category, content) VALUES (?, ?)",
        (category, content)
    )
    db.commit()
    memory_id = cursor.lastrowid
    db.close()

    return jsonify({
        "status": "remembered",
        "id": memory_id
    })


@app.get("/memories")
def memories():
    db = connect_db()

    rows = db.execute("""
        SELECT id, category, content, created_at
        FROM memories
        ORDER BY id DESC
        LIMIT 50
    """).fetchall()

    db.close()

    return jsonify([
        {
            "id": row[0],
            "category": row[1],
            "content": row[2],
            "created_at": row[3]
        }
        for row in rows
    ])


if __name__ == "__main__":
    connect_db().close()
    app.run(host="0.0.0.0", port=8765)
