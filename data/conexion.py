"""Utilidades de conexión SQLite compartidas por los módulos CRUD."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Optional


def obtener_ruta_bd() -> Path:
    """Devuelve la ruta absoluta del archivo de base de datos a utilizar.

    Prioriza la variable de entorno ``BIBLIOTECA_DB_PATH``. Si no está definida,
    busca un archivo ``admin_unificado.db`` en la carpeta ``BD_proyecto``;
    en su defecto, utiliza ``library.db`` ubicado en la raíz del proyecto.
    """
    valor_entorno: Optional[str] = os.environ.get("BIBLIOTECA_DB_PATH")
    if valor_entorno:
        return Path(valor_entorno).expanduser().resolve()

    raiz = Path(__file__).resolve().parent.parent
    candidato = raiz / "BD_proyecto" / "admin_unificado.db"
    if candidato.exists():
        return candidato

    return raiz / "library.db"


def obtener_conexion() -> sqlite3.Connection:
    """Crea una conexión a SQLite con claves foráneas habilitadas."""
    ruta = obtener_ruta_bd()
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion


__all__ = ["obtener_conexion", "obtener_ruta_bd"]
