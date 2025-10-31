"""Operaciones específicas de préstamos sobre las tablas ``loans`` y ``loan_items``."""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime
from typing import List

from models import Loan, LoanItem, LoanRequestItem, OperationResult

from .conexion import obtener_conexion


def listar_prestamos_activos() -> List[Loan]:
    """Devuelve los préstamos abiertos junto con sus ítems asociados."""
    with obtener_conexion() as conexion:
        prestamos_rows = conexion.execute(
            "SELECT * FROM loans WHERE status = 'active' ORDER BY created_at DESC"
        ).fetchall()

        prestamos: List[Loan] = []
        for fila in prestamos_rows:
            items_rows = conexion.execute(
                "SELECT * FROM loan_items WHERE loan_id = ?", (fila["id"],)
            ).fetchall()
            items = [
                LoanItem(
                    item_id=item_row["item_id"],
                    item_name=item_row["item_name"],
                    category=item_row["category"],
                    quantity=item_row["quantity"],
                )
                for item_row in items_rows
            ]
            prestamos.append(
                Loan(
                    id=fila["id"],
                    borrower_name=fila["borrower_name"],
                    loan_date=fila["loan_date"],
                    loan_time=fila["loan_time"],
                    expected_return_date=fila["return_date"],
                    expected_return_time=fila["return_time"],
                    status=fila["status"],
                    created_at=fila["created_at"],
                    items=items,
                )
            )
    return prestamos


def crear_prestamo(
    *,
    solicitante: str,
    fecha_prestamo: str,
    hora_prestamo: str,
    fecha_devolucion: str,
    hora_devolucion: str,
    articulos: List[LoanRequestItem],
) -> OperationResult:
    """Registra un préstamo con sus ítems y actualiza la disponibilidad."""
    if not articulos:
        return OperationResult.fail("No se seleccionaron artículos.")

    hora_prestamo = hora_prestamo or None
    hora_devolucion = hora_devolucion or None

    conexion = obtener_conexion()
    transaccion_activa = False

    try:
        for solicitud in articulos:
            fila = conexion.execute(
                "SELECT available_quantity FROM items WHERE id = ?", (solicitud.item.id,)
            ).fetchone()
            if not fila:
                return OperationResult.fail(f"El artículo '{solicitud.item.name}' no existe.")
            if fila["available_quantity"] < solicitud.quantity:
                disponible = fila["available_quantity"]
                return OperationResult.fail(
                    f"No hay stock suficiente de '{solicitud.item.name}'. Disponible: {disponible}."
                )

        prestamo_id = f"loan_{uuid.uuid4().hex[:10]}"
        creado_en = datetime.utcnow().isoformat()

        conexion.execute("BEGIN")
        transaccion_activa = True

        conexion.execute(
            """
            INSERT INTO loans (
                id, borrower_name, loan_date, loan_time,
                return_date, return_time, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?)
            """,
            (
                prestamo_id,
                solicitante,
                fecha_prestamo,
                hora_prestamo,
                fecha_devolucion,
                hora_devolucion,
                creado_en,
            ),
        )

        for solicitud in articulos:
            conexion.execute(
                """
                INSERT INTO loan_items (loan_id, item_id, item_name, category, quantity)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    prestamo_id,
                    solicitud.item.id,
                    solicitud.item.name,
                    solicitud.item.category,
                    solicitud.quantity,
                ),
            )

            fila_item = conexion.execute(
                "SELECT quantity, available_quantity FROM items WHERE id = ?",
                (solicitud.item.id,),
            ).fetchone()

            nuevo_disponible = fila_item["available_quantity"] - solicitud.quantity
            nuevo_estado = "Disponible" if nuevo_disponible > 0 else "Prestado"

            conexion.execute(
                "UPDATE items SET available_quantity = ?, status = ? WHERE id = ?",
                (nuevo_disponible, nuevo_estado, solicitud.item.id),
            )

        conexion.commit()
        transaccion_activa = False
        return OperationResult.ok()
    except sqlite3.Error as exc:
        if transaccion_activa:
            conexion.rollback()
        return OperationResult.fail(str(exc))
    finally:
        conexion.close()


def registrar_devolucion_prestamo(prestamo: Loan) -> OperationResult:
    """Registra la devolución de un préstamo activo y actualiza inventario."""
    conexion = obtener_conexion()
    transaccion_activa = False
    ahora = datetime.utcnow()
    devolucion_id = f"return_{uuid.uuid4().hex[:10]}"

    try:
        conexion.execute("BEGIN")
        transaccion_activa = True

        for detalle in prestamo.items:
            fila_item = conexion.execute(
                "SELECT quantity, available_quantity FROM items WHERE id = ?",
                (detalle.item_id,),
            ).fetchone()

            if not fila_item:
                continue

            nuevo_disponible = min(
                fila_item["quantity"], fila_item["available_quantity"] + detalle.quantity
            )
            nuevo_estado = "Disponible" if nuevo_disponible > 0 else "Prestado"

            conexion.execute(
                "UPDATE items SET available_quantity = ?, status = ? WHERE id = ?",
                (nuevo_disponible, nuevo_estado, detalle.item_id),
            )

        conexion.execute(
            "UPDATE loans SET status = 'returned' WHERE id = ?",
            (prestamo.id,),
        )

        items_payload = [
            {
                "item_id": detalle.item_id,
                "name": detalle.item_name,
                "category": detalle.category,
                "quantity": detalle.quantity,
            }
            for detalle in prestamo.items
        ]
        categorias = sorted({entrada["category"] for entrada in items_payload})

        conexion.execute(
            """
            INSERT INTO returns (
                id, loan_id, borrower_name, loan_date, loan_time,
                return_date, return_time, items_json, categories_json, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                devolucion_id,
                prestamo.id,
                prestamo.borrower_name,
                prestamo.loan_date,
                prestamo.loan_time,
                ahora.date().isoformat(),
                ahora.strftime("%H:%M"),
                json.dumps(items_payload),
                json.dumps(categorias),
                ahora.isoformat(),
            ),
        )

        conexion.commit()
        transaccion_activa = False
        return OperationResult.ok()
    except sqlite3.Error as exc:
        if transaccion_activa:
            conexion.rollback()
        return OperationResult.fail(str(exc))
    finally:
        conexion.close()


__all__ = [
    "listar_prestamos_activos",
    "crear_prestamo",
    "registrar_devolucion_prestamo",
]
