from __future__ import annotations

from typing import Optional

import flet as ft


class ScrollArea(ft.Container):
    """Contenedor con desplazamiento vertical reutilizable."""

    def __init__(
        self,
        content: ft.Control,
        *,
        expand: bool = True,
        padding: Optional[ft.PaddingValue] = None,
        bgcolor: Optional[str] = None,
        scroll_mode: ft.ScrollMode = ft.ScrollMode.AUTO,
    ) -> None:
        wrapper = ft.Column(
            controls=[content],
            expand=True,
            spacing=0,
            scroll=scroll_mode,
        )

        super().__init__(
            expand=expand,
            padding=padding,
            bgcolor=bgcolor,
            content=wrapper,
        )


__all__ = ["ScrollArea"]
