"""Paquete de acceso a datos (SQLite)."""

from .database import Database, asegurar_esquema

__all__ = ["Database", "asegurar_esquema"]
