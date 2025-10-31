from __future__ import annotations

from typing import Callable, Dict

import flet as ft

from screens import construir_vista_inicio_sesion, build_dashboard_view


RouteBuilder = Callable[[], ft.View]


class Router:
    """Gestiona la navegación declarativa entre pantallas."""

    def __init__(self, page: ft.Page, state: "AppState") -> None:
        self.page = page
        self.state = state
        self._routes: Dict[str, RouteBuilder] = {}

        self._register_routes()
        self._configure_page()

    # ------------------------------------------------------------------ #
    # Configuración inicial
    # ------------------------------------------------------------------ #
    def _register_routes(self) -> None:
        self._routes = {
            "/": lambda: construir_vista_inicio_sesion(self, self.state),
            "/dashboard": lambda: build_dashboard_view(self, self.state),
        }

    def _configure_page(self) -> None:
        self.page.on_route_change = self._handle_route_change
        self.page.on_view_pop = self._handle_view_pop
        # Arrancamos en la ruta actual (Flet envía "/" por defecto)
        self.go(self.page.route or "/")

    # ------------------------------------------------------------------ #
    # API pública
    # ------------------------------------------------------------------ #
    def go(self, route: str) -> None:
        """Lanza navegación a la ruta indicada."""
        if route not in self._routes:
            route = "/"
        self.page.go(route)

    def replace(self, route: str) -> None:
        """Reemplaza la vista actual (útil tras login/logout)."""
        if route not in self._routes:
            route = "/"
        self.page.views.clear()
        self.page.views.append(self._routes[route]())
        self.page.update()

    # ------------------------------------------------------------------ #
    # Callbacks de Flet
    # ------------------------------------------------------------------ #
    def _handle_route_change(self, route_change: ft.RouteChangeEvent) -> None:
        builder = self._routes.get(route_change.route, self._routes["/"])
        new_view = builder()
        self.page.views.clear()
        self.page.views.append(new_view)
        self.page.update()

    def _handle_view_pop(self, _: ft.ViewPopEvent) -> None:
        if self.page.views:
            self.page.views.pop()
        if not self.page.views:
            # Siempre garantizamos al menos la vista raíz
            self.page.views.append(self._routes["/"]())
        self.page.update()
