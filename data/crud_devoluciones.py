"""Operaciones relacionadas con la tabla ``returns``."""

from __future__ import annotations

import json
import sqlite3
from typing import List

from models import LoanItem, LoanReturn, OperationResult

from .conexion import obtener_conexion


def listar_devoluciones() -> List[LoanReturn]:
    """Devuelve el historial de devoluciones ordenado por fecha de creación."""
    with obtener_conexion() as conexion:
        filas = conexion.execute("SELECT * FROM returns ORDER BY created_at DESC").fetchall()

    resultados: List[LoanReturn] = []
    for fila in filas:
        items_payload = json.loads(fila["items_json"])
        items = [
            LoanItem(
                item_id=item["item_id"],
                item_name=item["name"],
                category=item["category"],
                quantity=item["quantity"],
            )
            for item in items_payload
        ]
        categorias = json.loads(fila["categories_json"]) if fila["categories_json"] else []

        resultados.append(
            LoanReturn(
                id=fila["id"],
                borrower_name=fila["borrower_name"],
                loan_date=fila["loan_date"],
                loan_time=fila["loan_time"],
                return_date=fila["return_date"],
                return_time=fila["return_time"],
                items=items,
                categories=categorias,
                created_at=fila["created_at"],
            )
        )
    return resultados


def eliminar_devolucion(identificador: str) -> OperationResult:
    """Elimina una devolución registrada."""
    try:
        with obtener_conexion() as conexion:
            conexion.execute("DELETE FROM returns WHERE id = ?", (identificador,))
        return OperationResult.ok()
    except sqlite3.Error as exc:
        return OperationResult.fail(str(exc))


__all__ = ["listar_devoluciones", "eliminar_devolucion"]
