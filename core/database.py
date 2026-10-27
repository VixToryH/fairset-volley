from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "fairset.db"

def create_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK (length(trim(name)) > 0),

                primary_position TEXT NOT NULL
                    CHECK (primary_position IN (
                        'SETTER', 'OUTSIDE', 'MIDDLE', 'OPPOSITE', 'LIBERO'
                    )),

                secondary_position TEXT
                    CHECK (
                        secondary_position IS NULL
                        OR secondary_position IN (
                            'SETTER', 'OUTSIDE', 'MIDDLE', 'OPPOSITE', 'LIBERO'
                        )
                    ),

                declared_level INTEGER NOT NULL
                    CHECK (declared_level BETWEEN 1 AND 10),

                mu REAL NOT NULL,
                sigma REAL NOT NULL DEFAULT 8
                    CHECK (sigma >= 2),

                games INTEGER NOT NULL DEFAULT 0 CHECK (games >= 0),
                wins INTEGER NOT NULL DEFAULT 0 CHECK (wins >= 0),
                losses INTEGER NOT NULL DEFAULT 0 CHECK (losses >= 0),

                CHECK (
                    secondary_position IS NULL
                    OR secondary_position != primary_position
                ),
                CHECK (wins + losses = games)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                winner TEXT
                    CHECK (winner IS NULL OR winner IN ('A', 'B')),

                p_a REAL
                    CHECK (p_a IS NULL OR p_a BETWEEN 0 AND 1)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS match_players (
                match_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,

                team TEXT NOT NULL
                    CHECK (team IN ('A', 'B')),

                position TEXT NOT NULL
                    CHECK (position IN (
                        'SETTER', 'OUTSIDE', 'MIDDLE', 'OPPOSITE', 'LIBERO'
                    )),

                mu_before REAL NOT NULL,
                mu_after REAL,
                sigma_before REAL NOT NULL,
                sigma_after REAL,

                PRIMARY KEY (match_id, player_id),

                FOREIGN KEY (match_id)
                    REFERENCES matches(id) ON DELETE CASCADE,

                FOREIGN KEY (player_id)
                    REFERENCES players(id)
            )
        """)

