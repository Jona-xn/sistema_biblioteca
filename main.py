import flet as ft

from app import AppState, Router
from data.conexion import obtener_ruta_bd
from data.database import Database, asegurar_esquema


def main(page: ft.Page) -> None:
    """Punto de entrada de la aplicación Flet."""
    page.title = "Sistema de Gestión de Biblioteca"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = "auto"
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START

    ruta_bd = obtener_ruta_bd()
    database = Database(str(ruta_bd))
    asegurar_esquema(database)

    app_state = AppState(page, database)
    Router(page, app_state)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
