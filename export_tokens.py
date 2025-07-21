#!/usr/bin/env python3
import sqlite3

DB_MASTER = "tickets_master.db"
DB_SCAN = "tickets_scan.db"

# Read tokens from master DB
m = sqlite3.connect(DB_MASTER)
c_master = m.cursor()
c_master.execute("SELECT token FROM tickets_master")
tokens = [row[0] for row in c_master.fetchall()]
m.close()

# Write tokens into scan DB
s = sqlite3.connect(DB_SCAN)
c_scan = s.cursor()
c_scan.execute("""
CREATE TABLE IF NOT EXISTS tickets_scan (
  token     TEXT PRIMARY KEY,
  used_flag INTEGER NOT NULL DEFAULT 0,
  used_at   DATETIME
)
""")
for token in tokens:
    c_scan.execute(
        "INSERT OR IGNORE INTO tickets_scan (token) VALUES (?)", (token,)
    )
s.commit()
s.close()
print(f"Exported {len(tokens)} tokens to '{DB_SCAN}'")
