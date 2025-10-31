"""Operaciones CRUD para la tabla ``admin``."""

from __future__ import annotations

from typing import List, Optional

from .conexion import obtener_conexion


def crear_tabla_admin() -> None:
    """Crea la tabla ``admin`` respetando el DER si aún no existe."""
    with obtener_conexion() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS admin (
                id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                correo TEXT NOT NULL,
                contrasena TEXT NOT NULL
            )
            """
        )


def registrar_admin(usuario: str, correo: str, contrasena: str) -> int:
    """Inserta un nuevo administrador y devuelve su ID."""
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            "INSERT INTO admin (usuario, correo, contrasena) VALUES (?, ?, ?)",
            (usuario, correo, contrasena),
        )
        return cursor.lastrowid


def obtener_admin_por_id(identificador: int) -> Optional[dict]:
    """Recupera un administrador específico."""
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            "SELECT id_admin, usuario, correo, contrasena FROM admin WHERE id_admin = ?",
            (identificador,),
        ).fetchone()
        return dict(fila) if fila else None


def listar_admins() -> List[dict]:
    """Devuelve la lista completa de administradores."""
    with obtener_conexion() as conexion:
        filas = conexion.execute(
            "SELECT id_admin, usuario, correo, contrasena FROM admin ORDER BY id_admin"
        ).fetchall()
        return [dict(fila) for fila in filas]


def obtener_admin_por_usuario(usuario: str) -> Optional[dict]:
    """Busca un administrador por su nombre de usuario."""
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            "SELECT id_admin, usuario, correo, contrasena FROM admin WHERE usuario = ?",
            (usuario,),
        ).fetchone()
        return dict(fila) if fila else None


def validar_credenciales_admin(usuario: str, contrasena: str) -> Optional[dict]:
    """Devuelve el administrador si usuario/contraseña coinciden."""
    admin = obtener_admin_por_usuario(usuario)
    if not admin:
        return None
    return admin if admin.get("contrasena") == contrasena else None


def actualizar_admin(
    identificador: int,
    *,
    usuario: Optional[str] = None,
    correo: Optional[str] = None,
    contrasena: Optional[str] = None,
) -> bool:
    """Actualiza los campos indicados del administrador."""
    campos = []
    valores = []
    if usuario is not None:
        campos.append("usuario = ?")
        valores.append(usuario)
    if correo is not None:
        campos.append("correo = ?")
        valores.append(correo)
    if contrasena is not None:
        campos.append("contrasena = ?")
        valores.append(contrasena)

    if not campos:
        return False

    valores.append(identificador)
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            f"UPDATE admin SET {', '.join(campos)} WHERE id_admin = ?",
            valores,
        )
        return cursor.rowcount > 0


def eliminar_admin(identificador: int) -> bool:
    """Elimina un administrador."""
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            "DELETE FROM admin WHERE id_admin = ?",
            (identificador,),
        )
        return cursor.rowcount > 0


__all__ = [
    "crear_tabla_admin",
    "registrar_admin",
    "obtener_admin_por_id",
    "obtener_admin_por_usuario",
    "validar_credenciales_admin",
    "listar_admins",
    "actualizar_admin",
    "eliminar_admin",
]
