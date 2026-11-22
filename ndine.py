"""
N-dine-lang Reference Engine (ndine.py)
Author: Kelly R. Morgan
Title: Assistant Professor of Information Technology
Affiliation: Navajo Technical University (Crownpoint, NM)
Year: 2026
License: MIT License
"""

import csv
import os
import re
import sqlite3
import subprocess
import unicodedata
from typing import Dict, List, Optional, Tuple

DEFAULT_DB_PATH = os.path.join("db", "dine_lang.db")


def load_env_file(path: str = ".env") -> None:
    """
    Loads KEY=VALUE pairs from a .env file into os.environ.

    Uses python-dotenv when installed (declared in requirements.txt) and falls
    back to a small built-in parser otherwise. Existing environment variables
    take precedence; blank lines and lines starting with '#' are ignored.
    """
    if not os.path.isfile(path):
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None
    if load_dotenv is not None:
        load_dotenv(path, override=False)
        return
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def get_gemini_api_key() -> Optional[str]:
    """
    Returns the Google Gemini API key from the environment or .env file.

    Environment variables take precedence over .env. Returns None when the
    key is unset or blank. This function performs no network calls.
    """
    load_env_file()
    value = os.environ.get("GEMINI_API_KEY", "").strip()
    return value or None


class NDineEngine:
    """
    Reference parser, SQLite lexicon manager, and command runner for N-dine-lang.
    Canonical Slot Order: T- (Tense/Time), S- (Subject), V- (Verb), O- (Object), L- (Location)
    Optional Control Prefixes: Q- (Query), M- (Mandatory/Imperative), C- (Condition), R- (Reason)
    """

    VALID_SLOTS = ("T", "S", "V", "O", "L", "Q", "M", "C", "R")

    def __init__(self, db_path: Optional[str] = None):
        """
        Database location. Defaults to DEFAULT_DB_PATH (db/dine_lang.db),
        inside the db/ directory created by bootstrap.py. Pass an explicit
        path to override it, which is useful for tests or alternate datasets.
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self.init_db()

    @staticmethod
    def to_plain_ascii(text: str) -> str:
        """
        Strips glottal stops, high-tone accents, nasal hooks, and barred-L characters
        to produce clean plain-ASCII Diné Bizaad text (a-z, 0-9, spaces, hyphens).
        """
        if not text:
            return ""
        text = text.replace("ł", "l").replace("Ł", "L")
        normalized = unicodedata.normalize("NFD", text)
        ascii_only = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
        cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", ascii_only)
        return " ".join(cleaned.split()).strip()

    @classmethod
    def parse(cls, sentence: str) -> Dict[str, str]:
        """
        Parses an N-dine-lang string into a dictionary keyed by role prefix.
        Example: 'T-pst S-boy V-see O-dog L-home.'
        Returns: {'T': 'pst', 'S': 'boy', 'V': 'see', 'O': 'dog', 'L': 'home'}
        """
        slots: Dict[str, str] = {}
        clean_sentence = sentence.strip().rstrip(".")
        for token in clean_sentence.split():
            prefix, sep, value = token.partition("-")
            if sep and prefix in cls.VALID_SLOTS:
                slots[prefix] = value
        return slots

    @classmethod
    def format_slots(cls, slots: Dict[str, str]) -> str:
        """
        Reconstructs a canonical N-dine-lang string in strict T-S-V-O-L order
        from a dictionary of slot values.
        """
        ordered_keys = ["Q", "M", "C", "T", "S", "V", "O", "L", "R"]
        tokens: List[str] = []
        for key in ordered_keys:
            val = slots.get(key, "").strip()
            if val:
                tokens.append(f"{key}-{val}")
        for key, val in slots.items():
            if key not in ordered_keys and key in cls.VALID_SLOTS and val.strip():
                tokens.append(f"{key}-{val.strip()}")
        return (" ".join(tokens) + ".") if tokens else ""

    def init_db(self) -> None:
        """Creates the SQLite lexicon table if it does not already exist."""
        parent = os.path.dirname(self.db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lexicon (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dine_raw TEXT,
                    dine_ascii TEXT,
                    english TEXT,
                    n_dine_full TEXT,
                    slot_t TEXT,
                    slot_s TEXT,
                    slot_v TEXT,
                    slot_o TEXT,
                    slot_l TEXT
                )
            """)
            conn.commit()

    def add_entry(
        self,
        dine_raw: str,
        english: str,
        n_dine_full: str,
        dine_ascii: Optional[str] = None,
    ) -> int:
        """Inserts a parallel Diné / English / N-dine-lang record into SQLite."""
        clean_ascii = dine_ascii if dine_ascii is not None else self.to_plain_ascii(dine_raw)
        slots = self.parse(n_dine_full)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO lexicon (
                    dine_raw, dine_ascii, english, n_dine_full,
                    slot_t, slot_s, slot_v, slot_o, slot_l
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    dine_raw.strip(),
                    clean_ascii,
                    english.strip(),
                    n_dine_full.strip(),
                    slots.get("T", ""),
                    slots.get("S", ""),
                    slots.get("V", ""),
                    slots.get("O", ""),
                    slots.get("L", ""),
                ),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def import_csv(
        self,
        csv_path: str,
        dine_col: str = "dine",
        english_col: str = "english",
        ndine_col: str = "n_dine",
    ) -> int:
        """
        Imports rows from a CSV file into the SQLite database.
        If the CSV does not yet contain an 'n_dine' column, inserts blank slot placeholders
        ready for AI batch translation.
        """
        count = 0
        with open(csv_path, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dine_val = row.get(dine_col, "")
                eng_val = row.get(english_col, "")
                ndine_val = row.get(ndine_col, "")
                if dine_val or eng_val:
                    self.add_entry(dine_raw=dine_val, english=eng_val, n_dine_full=ndine_val)
                    count += 1
        return count

    def search_lexicon(self, term: str) -> List[Tuple]:
        """Searches the SQLite lexicon across Diné ASCII, English, and N-dine-lang."""
        pattern = f"%{term}%"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT id, dine_ascii, english, n_dine_full
                FROM lexicon
                WHERE dine_ascii LIKE ? OR english LIKE ? OR n_dine_full LIKE ?
                """,
                (pattern, pattern, pattern),
            )
            return cursor.fetchall()

    def execute_command(self, command: str) -> Dict[str, object]:
        """
        Executes operational N-dine-lang instructions:
          - Query DB: Q-prs S-1sg V-find O-water L-lexicon.
          - Ping Host: M-now S-admin V-ping O-8.8.8.8 L-local.
        """
        slots = self.parse(command)
        action = slots.get("V", "")
        target = slots.get("O", "")

        if "Q" in slots and action == "find":
            matches = self.search_lexicon(target)
            return {"status": "ok", "action": "find", "target": target, "results": matches}

        if slots.get("M") == "now" and action == "ping" and target:
            flag = "-n" if os.name == "nt" else "-c"
            proc = subprocess.run(
                ["ping", flag, "2", target],
                capture_output=True,
                text=True,
            )
            return {
                "status": "ok" if proc.returncode == 0 else "error",
                "action": "ping",
                "target": target,
                "returncode": proc.returncode,
                "output": proc.stdout.strip(),
            }

        return {"status": "parsed", "slots": slots}


if __name__ == "__main__":
    engine = NDineEngine()

    # Seed sample entries if database is empty
    if not engine.search_lexicon("water"):
        engine.add_entry(
            dine_raw="Tó yishdlą́.",
            english="I am drinking water.",
            n_dine_full="T-prs S-1sg V-drink O-water.",
        )
        engine.add_entry(
            dine_raw="Ashkii łééchąąʼí yiyííłtsą́.",
            english="The boy saw the dog at home.",
            n_dine_full="T-pst S-boy V-see O-dog L-home.",
        )

    print("1. ASCII Sanitizer:", engine.to_plain_ascii("Tʼáá ákwíí abíní tó sikʼazí yishdlą́."))
    print("2. Slot Parser:", engine.parse("T-pst S-boy V-see O-dog L-home."))
    print("3. Query Command:", engine.execute_command("Q-prs S-1sg V-find O-water L-lexicon."))
