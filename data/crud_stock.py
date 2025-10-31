"""Operaciones CRUD para la tabla ``stock``."""

from __future__ import annotations

from typing import List, Optional

from .conexion import obtener_conexion


def crear_tabla_stock() -> None:
    """Crea la tabla ``stock`` si aún no existe."""
    with obtener_conexion() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS stock (
                id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
                cantidad_total INTEGER NOT NULL,
                cantidad_disponible INTEGER NOT NULL
            )
            """
        )


def registrar_stock(cantidad_total: int, cantidad_disponible: int) -> int:
    """Inserta un registro de stock y devuelve su ID."""
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            "INSERT INTO stock (cantidad_total, cantidad_disponible) VALUES (?, ?)",
            (cantidad_total, cantidad_disponible),
        )
        return cursor.lastrowid


def obtener_stock_por_id(identificador: int) -> Optional[dict]:
    """Devuelve un registro de stock específico."""
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            "SELECT id_stock, cantidad_total, cantidad_disponible FROM stock WHERE id_stock = ?",
            (identificador,),
        ).fetchone()
        return dict(fila) if fila else None


def listar_stock() -> List[dict]:
    """Lista todos los registros de stock."""
    with obtener_conexion() as conexion:
        filas = conexion.execute(
            "SELECT id_stock, cantidad_total, cantidad_disponible FROM stock ORDER BY id_stock"
        ).fetchall()
        return [dict(fila) for fila in filas]


def actualizar_stock(
    identificador: int,
    *,
    cantidad_total: Optional[int] = None,
    cantidad_disponible: Optional[int] = None,
) -> bool:
    """Actualiza los datos del stock indicado."""
    campos = []
    valores = []
    if cantidad_total is not None:
        campos.append("cantidad_total = ?")
        valores.append(cantidad_total)
    if cantidad_disponible is not None:
        campos.append("cantidad_disponible = ?")
        valores.append(cantidad_disponible)

    if not campos:
        return False

    valores.append(identificador)
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            f"UPDATE stock SET {', '.join(campos)} WHERE id_stock = ?",
            valores,
        )
        return cursor.rowcount > 0


def eliminar_stock(identificador: int) -> bool:
    """Elimina un registro de stock."""
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            "DELETE FROM stock WHERE id_stock = ?",
            (identificador,),
        )
        return cursor.rowcount > 0


__all__ = [
    "crear_tabla_stock",
    "registrar_stock",
    "obtener_stock_por_id",
    "listar_stock",
    "actualizar_stock",
    "eliminar_stock",
]
