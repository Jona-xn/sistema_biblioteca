from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from components.sidebar import Sidebar
from screens.registro_prestamo import LoanSection

if TYPE_CHECKING:
    from app.router import Router
    from app.state import AppState


class DashboardShell(ft.Row):
    """Contenedor principal del panel (sidebar + contenido)."""

    def __init__(self, router: "Router", state: "AppState") -> None:
        self.router = router
        self.state = state

        self.sidebar = Sidebar(on_change=self._handle_sidebar_selection)
        self.content = LoanSection(state)

        main_area = ft.Container(
            expand=True,
            bgcolor=ft.colors.BLUE_GREY_50,
            content=ft.Container(
                expand=True,
                padding=ft.padding.all(24),
                content=self.content,
            ),
        )

        super().__init__(controls=[self.sidebar, main_area], expand=True, spacing=0)

    def _handle_sidebar_selection(self, key: str) -> None:
        if key == "logout":
            self.state.clear_session()
            self.router.replace("/")
            self.state.notify("Sesión cerrada correctamente.", kind="info")
            return
        if key == "loan":
            self.sidebar.set_active("loan")
            return

        self.state.notify("Sección en desarrollo. Estará disponible próximamente.", kind="info")
        self.sidebar.set_active("loan")


def build_dashboard_view(router: "Router", state: "AppState") -> ft.View:
    shell = DashboardShell(router, state)
    return ft.View(route="/dashboard", controls=[shell], padding=0)
