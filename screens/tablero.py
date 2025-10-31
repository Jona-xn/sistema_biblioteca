import flet as ft
from typing import TYPE_CHECKING
from screens.registro_prestamo import LoanSection

if TYPE_CHECKING:
    from app.router import Router
    from app.state import AppState

def build_dashboard_view(router: "Router", state: "AppState") -> ft.View:
    contenido = LoanSection(state)
    return ft.View(route="/dashboard", controls=[contenido], padding=0)
