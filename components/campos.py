from __future__ import annotations

import flet as ft


def crear_campo_texto(
    etiqueta: str,
    pista: str,
    icono: str,
    *,
    es_password: bool = False,
    revelar_password: bool = True,
    autofoco: bool = False,
) -> ft.TextField:
    """Genera un campo de texto consistente para formularios."""
    return ft.TextField(
        label=etiqueta,
        hint_text=pista,
        prefix_icon=icono,
        border_radius=12,
        password=es_password,
        can_reveal_password=revelar_password if es_password else False,
        autofocus=autofoco,
    )
