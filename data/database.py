from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import Optional

from models import User


class Database:
    """Encapsula la conexión principal a SQLite y utilidades básicas."""

    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def cerrar(self) -> None:
        """Cierra la conexión abierta."""
        self._conn.close()

    def autenticar_usuario(self, usuario: str, contrasena: str) -> Optional[User]:
        """Valida credenciales contra la tabla ``users``."""
        fila = self._conn.execute(
            "SELECT username, full_name, password_hash FROM users WHERE username = ?",
            (usuario,),
        ).fetchone()
        if not fila:
            return None
        if fila["password_hash"] != self._hash_password(contrasena):
            return None
        return User(username=fila["username"], full_name=fila["full_name"])


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    full_name TEXT
);

CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    quantity INTEGER NOT NULL,
    available_quantity INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loans (
    id TEXT PRIMARY KEY,
    borrower_name TEXT NOT NULL,
    loan_date TEXT NOT NULL,
    loan_time TEXT,
    return_date TEXT NOT NULL,
    return_time TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS loan_items (
    loan_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (loan_id, item_id),
    FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS returns (
    id TEXT PRIMARY KEY,
    loan_id TEXT NOT NULL,
    borrower_name TEXT NOT NULL,
    loan_date TEXT NOT NULL,
    loan_time TEXT,
    return_date TEXT NOT NULL,
    return_time TEXT,
    items_json TEXT NOT NULL,
    categories_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
);
"""


def asegurar_esquema(base_datos: Database) -> None:
    """Crea la estructura base y el usuario administrador por defecto."""
    base_datos._conn.executescript(SCHEMA_SQL)
    base_datos._conn.commit()

    admin = base_datos._conn.execute(
        "SELECT username FROM users WHERE username = 'admin'"
    ).fetchone()
    if not admin:
        base_datos._conn.execute(
            "INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)",
            ("admin", base_datos._hash_password("admin123"), "Administrador"),
        )
        base_datos._conn.commit()


__all__ = ["Database", "asegurar_esquema"]
