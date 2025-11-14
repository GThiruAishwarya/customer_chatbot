# backend/db_setup.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "faq.db")

SAMPLE_FAQS = [
    ("What products do you sell?", "We sell snacks, sauces, and drinks."),
    ("Where are your physical stores located?", "We are an online-only business and do not have physical stores."),
    ("What is your return policy?", "You can return any product within 30 days for a full refund."),
    ("How can I contact customer support?", "Email us at support@example.com or call (555) 123-4567."),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            bot_msg TEXT,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("SELECT COUNT(1) FROM faq")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany("INSERT INTO faq (question, answer) VALUES (?, ?)", SAMPLE_FAQS)
        print(f"Inserted {len(SAMPLE_FAQS)} sample FAQs.")
    else:
        print(f"FAQ table already has {count} rows. Skipping sample insert.")

    conn.commit()
    conn.close()
    print("Database initialized at:", DB_PATH)

if __name__ == "__main__":
    init_db()
