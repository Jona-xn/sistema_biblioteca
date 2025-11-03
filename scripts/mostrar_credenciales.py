from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from data.conexion import obtener_ruta_bd


def main() -> None:
    ruta_bd = obtener_ruta_bd()
    conn = sqlite3.connect(ruta_bd)
    conn.row_factory = sqlite3.Row
    filas = conn.execute('SELECT usuario, contrasena FROM admin ORDER BY usuario').fetchall()
    conn.close()

    print('Recuperación express solicitada por el cliente.')
    print('ATENCIÓN: Este procedimiento es inseguro y se implementó solo a petición del cliente.')
    print(f'Archivo de base de datos: {ruta_bd}')
    print('\nCredenciales registradas:')
    if not filas:
        print('  (no se encontraron registros en la tabla admin)')
    for fila in filas:
        print(f"  Usuario: {fila['usuario']!r}  |  Contraseña: {fila['contrasena']!r}")
    print('\nPresiona Enter para cerrar esta ventana...')
    input()


if __name__ == '__main__':
    main()
