from __future__ import annotations

import flet as ft


def crear_boton_principal(
    texto: str,
    icono: str,
    *,
    expandir: bool = True,
    alto: int = 48,
    evento: ft.ControlEventHandler | None = None,
) -> ft.ElevatedButton:
    """Construye un botón primario reutilizable con estilo consistente."""
    return ft.ElevatedButton(
        text=texto,
        icon=icono,
        expand=expandir,
        height=alto,
        style=ft.ButtonStyle(
            color={ft.ControlState.DEFAULT: ft.colors.WHITE},
            bgcolor={
                ft.ControlState.DEFAULT: ft.colors.BLUE_700,
                ft.ControlState.HOVERED: ft.colors.BLUE_800,
            },
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=evento,
    )
