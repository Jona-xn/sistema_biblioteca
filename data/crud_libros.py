"""Operaciones CRUD para la tabla ``libros``."""

from __future__ import annotations

from typing import List, Optional

from .conexion import obtener_conexion

COLUMNAS_LIBRO = [
    "codigo",
    "id_inventario",
    "signatura_topografica",
    "ubicacion",
    "tipo_de_ficha",
    "responsabilidad_personal",
    "otra_responsabilidad",
    "titulo_y_subtitulo",
    "datos_de_edicion",
    "lugar",
    "editor_distribuidor",
    "anio_edicion",
    "descripcion_fisica",
    "serie_subserie",
    "numero_serie_subserie",
    "isbn",
    "contenido",
    "materia",
    "estado",
    "bibliotecario",
    "operador",
]


def crear_tabla_libros() -> None:
    """Crea la tabla ``libros`` si aún no existe."""
    with obtener_conexion() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS libros (
                codigo TEXT PRIMARY KEY,
                id_inventario INTEGER REFERENCES inventario(id_inventario),
                signatura_topografica TEXT,
                ubicacion TEXT,
                tipo_de_ficha TEXT,
                responsabilidad_personal TEXT,
                otra_responsabilidad TEXT,
                titulo_y_subtitulo TEXT,
                datos_de_edicion TEXT,
                lugar TEXT,
                editor_distribuidor TEXT,
                anio_edicion TEXT,
                descripcion_fisica TEXT,
                serie_subserie TEXT,
                numero_serie_subserie TEXT,
                isbn TEXT,
                contenido TEXT,
                materia TEXT,
                estado TEXT,
                bibliotecario TEXT,
                operador TEXT
            )
            """
        )


def registrar_libro(**datos: Optional[str]) -> str:
    """Inserta un registro en ``libros``. El parámetro ``codigo`` es obligatorio."""
    if "codigo" not in datos or not datos["codigo"]:
        raise ValueError("El campo 'codigo' es obligatorio para registrar un libro.")

    valores = [datos.get(campo) for campo in COLUMNAS_LIBRO]
    with obtener_conexion() as conexion:
        conexion.execute(
            f"""
            INSERT INTO libros ({', '.join(COLUMNAS_LIBRO)})
            VALUES ({', '.join(['?'] * len(COLUMNAS_LIBRO))})
            """,
            valores,
        )
    return str(datos["codigo"])


def obtener_libro_por_codigo(codigo: str) -> Optional[dict]:
    """Obtiene un libro concreto a partir de su código."""
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            f"""
            SELECT {', '.join(COLUMNAS_LIBRO)}
            FROM libros
            WHERE codigo = ?
            """,
            (codigo,),
        ).fetchone()
        return dict(fila) if fila else None


def listar_libros(limit: Optional[int] = None, offset: int = 0) -> List[dict]:
    """Devuelve la lista de libros. Permite limitar y desplazarse con ``offset``."""
    if limit is not None and limit <= 0:
        limit = None
    if offset < 0:
        offset = 0

    consulta = f"SELECT {', '.join(COLUMNAS_LIBRO)} FROM libros ORDER BY codigo"
    with obtener_conexion() as conexion:
        if limit is not None:
            filas = conexion.execute(consulta + " LIMIT ? OFFSET ?", (limit, offset)).fetchall()
        else:
            filas = conexion.execute(consulta).fetchall()
        return [dict(fila) for fila in filas]


def actualizar_libro(codigo: str, **datos: Optional[str]) -> bool:
    """Actualiza los campos proporcionados del libro identificado por ``codigo``."""
    campos = []
    valores = []
    for campo, valor in datos.items():
        if campo in COLUMNAS_LIBRO and campo != "codigo" and valor is not None:
            campos.append(f"{campo} = ?")
            valores.append(valor)

    if not campos:
        return False

    valores.append(codigo)
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            f"UPDATE libros SET {', '.join(campos)} WHERE codigo = ?",
            valores,
        )
        return cursor.rowcount > 0


def eliminar_libro(codigo: str) -> bool:
    """Borra un libro del catálogo."""
    with obtener_conexion() as conexion:
        cursor = conexion.execute(
            "DELETE FROM libros WHERE codigo = ?",
            (codigo,),
        )
        return cursor.rowcount > 0


def contar_libros() -> int:
    """Cantidad total de libros registrados."""
    with obtener_conexion() as conexion:
        resultado = conexion.execute("SELECT COUNT(*) FROM libros").fetchone()
        return int(resultado[0]) if resultado else 0


__all__ = [
    "crear_tabla_libros",
    "registrar_libro",
    "obtener_libro_por_codigo",
    "listar_libros",
    "actualizar_libro",
    "eliminar_libro",
    "contar_libros",
]
