from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import flet as ft


@dataclass
class Session:
    """Representa el estado de sesión del usuario autenticado."""

    username: Optional[str] = None
    display_name: Optional[str] = None

    @property
    def is_authenticated(self) -> bool:
        return self.username is not None


class AppState:
    """Mantiene referencias compartidas (página, base de datos, sesión, etc.)."""

    def __init__(self, page: ft.Page, db: "Database") -> None:
        self.page = page
        self.db = db
        self.session = Session()

    # --------------------------------------------------------------------- #
    # Utilidades de UI
    # --------------------------------------------------------------------- #
    def notify(self, message: str, *, kind: str = "success") -> None:
        """Muestra un snackbar reutilizable."""
        color = {
            "success": ft.colors.GREEN_600,
            "error": ft.colors.RED_600,
            "info": ft.colors.BLUE_600,
        }.get(kind, ft.colors.BLUE_600)

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=color,
            action="Cerrar",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def set_session(self, username: str, display_name: Optional[str] = None) -> None:
        """Actualiza la sesión y refresca la página."""
        self.session.username = username
        self.session.display_name = display_name or username.title()
        self.page.update()

    def clear_session(self) -> None:
        """Cierra sesión del usuario actual."""
        self.session = Session()
        self.page.update()
