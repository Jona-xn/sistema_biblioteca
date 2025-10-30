from __future__ import annotations

import app  # noqa: F401  # asegura la compatibilidad de Flet
import flet as ft
from flet import Colors

from screens.inicio_sesion import construir_vista_inicio_sesion


class EstadoVistaPrevia:
    """Estado mínimo para mostrar la pantalla en modo maqueta."""

    es_vista_previa = True

    def __init__(self, pagina: ft.Page) -> None:
        self.page = pagina

    def notify(self, mensaje: str, *, kind: str = "info") -> None:
        colores = {
            "success": Colors.GREEN_600.value,
            "error": Colors.RED_600.value,
            "info": Colors.BLUE_600.value,
        }
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color=Colors.WHITE.value),
            bgcolor=colores.get(kind, Colors.BLUE_600.value),
        )
        self.page.snack_bar.open = True
        self.page.update()


class EnrutadorNulo:
    """Stub sin navegación real (solo requerido por la vista)."""

    es_vista_previa = True


def main(pagina: ft.Page) -> None:
    pagina.title = "Vista previa – Inicio de sesión"
    pagina.padding = 0
    pagina.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    pagina.vertical_alignment = ft.MainAxisAlignment.START

    estado = EstadoVistaPrevia(pagina)
    enrutador = EnrutadorNulo()
    vista = construir_vista_inicio_sesion(enrutador, estado)

    pagina.views.clear()
    pagina.views.append(vista)
    pagina.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
