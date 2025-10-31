"""Operaciones específicas de inventario sobre la tabla ``items``."""

from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime
from typing import List

from models import Item, ItemCreateRequest, OperationResult

from .conexion import obtener_conexion


def _fila_a_articulo(fila: sqlite3.Row) -> Item:
    return Item(
        id=fila["id"],
        name=fila["name"],
        category=fila["category"],
        description=fila["description"],
        quantity=fila["quantity"],
        available_quantity=fila["available_quantity"],
        status=fila["status"],
        created_at=fila["created_at"],
    )


def listar_articulos() -> List[Item]:
    """Devuelve todos los artículos del inventario ordenados por creación."""
    with obtener_conexion() as conexion:
        filas = conexion.execute("SELECT * FROM items ORDER BY created_at DESC").fetchall()
    return [_fila_a_articulo(fila) for fila in filas]


def listar_articulos_disponibles() -> List[Item]:
    """Obtiene únicamente los artículos con disponibilidad mayor que cero."""
    with obtener_conexion() as conexion:
        filas = conexion.execute(
            "SELECT * FROM items WHERE available_quantity > 0 ORDER BY name"
        ).fetchall()
    return [_fila_a_articulo(fila) for fila in filas]


def crear_articulo(solicitud: ItemCreateRequest) -> OperationResult:
    """Registra un artículo junto con su stock inicial."""
    articulo_id = f"item_{uuid.uuid4().hex[:8]}"
    creado_en = datetime.utcnow().isoformat()
    estado = solicitud.status or ("Disponible" if solicitud.quantity > 0 else "Prestado")

    try:
        with obtener_conexion() as conexion:
            conexion.execute(
                """
                INSERT INTO items (
                    id, name, category, description, quantity,
                    available_quantity, status, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    articulo_id,
                    solicitud.name,
                    solicitud.category,
                    solicitud.description,
                    solicitud.quantity,
                    solicitud.quantity,
                    estado,
                    creado_en,
                ),
            )
        return OperationResult.ok()
    except sqlite3.Error as exc:
        return OperationResult.fail(str(exc))


def actualizar_articulo(articulo_id: str, solicitud: ItemCreateRequest) -> OperationResult:
    """Actualiza la información y disponibilidad de un artículo existente."""
    try:
        with obtener_conexion() as conexion:
            fila = conexion.execute(
                "SELECT quantity, available_quantity FROM items WHERE id = ?", (articulo_id,)
            ).fetchone()
            if not fila:
                return OperationResult.fail("El artículo no existe.")

            prestados = fila["quantity"] - fila["available_quantity"]
            disponible = max(0, solicitud.quantity - prestados)
            estado = solicitud.status or ("Disponible" if disponible > 0 else "Prestado")

            conexion.execute(
                """
                UPDATE items
                SET name = ?, category = ?, description = ?, quantity = ?,
                    available_quantity = ?, status = ?
                WHERE id = ?
                """,
                (
                    solicitud.name,
                    solicitud.category,
                    solicitud.description,
                    solicitud.quantity,
                    disponible,
                    estado,
                    articulo_id,
                ),
            )
        return OperationResult.ok()
    except sqlite3.Error as exc:
        return OperationResult.fail(str(exc))


def eliminar_articulo(articulo_id: str) -> OperationResult:
    """Elimina un artículo si no tiene préstamos activos asociados."""
    try:
        with obtener_conexion() as conexion:
            prestamos_activos = conexion.execute(
                """
                SELECT COUNT(*)
                FROM loan_items li
                JOIN loans l ON l.id = li.loan_id
                WHERE li.item_id = ? AND l.status = 'active'
                """,
                (articulo_id,),
            ).fetchone()[0]

            if prestamos_activos:
                return OperationResult.fail("El artículo tiene préstamos activos. No se puede eliminar.")

            conexion.execute("DELETE FROM items WHERE id = ?", (articulo_id,))
        return OperationResult.ok()
    except sqlite3.Error as exc:
        return OperationResult.fail(str(exc))


__all__ = [
    "listar_articulos",
    "listar_articulos_disponibles",
    "crear_articulo",
    "actualizar_articulo",
    "eliminar_articulo",
]
