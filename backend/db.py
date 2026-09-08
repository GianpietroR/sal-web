"""Gestione database SQLite per SAL Web.

Il database è un unico file (data/sal.db): il backup è una copia di quel file.
I dati contrattuali (voci_computo con origine='contrattuale') non vengono mai
scritti dalle routine di avanzamento: la separazione è garantita a livello di
codice, non solo di interfaccia.
"""
import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DB_DIR / "sal.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  salt TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now'))
);

CREATE TABLE IF NOT EXISTS sessions (
  token TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now'))
);

-- Schede cantiere: ogni cantiere è indipendente (multi-cantiere).
CREATE TABLE IF NOT EXISTS cantieri (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  committente TEXT DEFAULT '',
  impresa TEXT DEFAULT '',
  tecnico TEXT DEFAULT '',
  oggetto TEXT DEFAULT '',
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
  updated_at TEXT
);

-- Unico computo vivo: capitoli, sottocapitoli e voci contrattuali +
-- lavorazioni fuori capitolato (origine='fuori_capitolato'), visivamente
-- distinte ma gestite con la stessa logica di avanzamento.
CREATE TABLE IF NOT EXISTS voci_computo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cantiere_id INTEGER NOT NULL REFERENCES cantieri(id),
  posizione INTEGER NOT NULL,
  tipo TEXT NOT NULL DEFAULT 'voce' CHECK (tipo IN ('capitolo','sotto_capitolo','voce')),
  origine TEXT NOT NULL DEFAULT 'contrattuale' CHECK (origine IN ('contrattuale','fuori_capitolato')),
  categoria_fuori TEXT,
  codice TEXT,
  descrizione TEXT NOT NULL,
  um TEXT,
  quantita_reale REAL,
  prezzo_unitario REAL,
  importo_reale REAL
);

-- Ogni SAL è una fotografia: numero univoco per cantiere, stato aperto/congelato.
CREATE TABLE IF NOT EXISTS sal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cantiere_id INTEGER NOT NULL REFERENCES cantieri(id),
  numero INTEGER NOT NULL,
  data TEXT NOT NULL,
  periodo TEXT DEFAULT '',
  note TEXT DEFAULT '',
  stato TEXT NOT NULL DEFAULT 'aperto' CHECK (stato IN ('aperto','congelato')),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
  UNIQUE (cantiere_id, numero)
);

-- Snapshot per voce: memorizza la quantità PROGRESSIVA e l'importo già calcolato.
-- I SAL congelati sono solo-lettura (garanzia a livello di codice).
CREATE TABLE IF NOT EXISTS avanzamento_voce (
  sal_id INTEGER NOT NULL REFERENCES sal(id),
  voce_id INTEGER NOT NULL REFERENCES voci_computo(id),
  quantita_progressiva REAL NOT NULL DEFAULT 0,
  importo_eseguito REAL NOT NULL DEFAULT 0,
  PRIMARY KEY (sal_id, voce_id)
);

CREATE INDEX IF NOT EXISTS idx_voci_cantiere ON voci_computo(cantiere_id, posizione);
CREATE INDEX IF NOT EXISTS idx_avv_sal ON avanzamento_voce(sal_id);
"""


def get_conn() -> sqlite3.Connection:
    """Connessione con row factory e foreign key attive. Chiama close()."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Crea tabelle e indici se non esistono (idempotente)."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.commit()
    finally:
        conn.close()
