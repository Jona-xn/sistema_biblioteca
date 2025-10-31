"""Inicializa el paquete de la aplicación para el sistema de gestión bibliotecaria."""

import flet as ft
from flet import Colors, Icons

# TODO: La capa de compatibilidad puede eliminarse cuando el proyecto migre
#       por completo a la API moderna de Flet (los enums de colores/íconos se
#       movieron a submódulos desde la versión 0.28). Mantenerla aquí garantiza
#       que las vistas antiguas y las previsualizaciones sigan encontrando
#       `ft.colors` y `ft.icons` sin romper los flujos actuales.


def _ensure_colors_compat() -> None:
    if hasattr(ft, "colors"):
        return

    class _ColorsCompat:
        def __getattr__(self, name: str):
            attr = getattr(Colors, name)
            if isinstance(attr, Colors):
                return attr.value
            return attr

        def with_opacity(self, opacity: float, color) -> str:
            token = None
            if isinstance(color, Colors):
                token = color
            elif isinstance(color, str):
                upper = color.upper()
                if upper in Colors.__members__:
                    token = Colors[upper]
                else:
                    return f"{color},{opacity}"
            else:
                return f"{color},{opacity}"
            return Colors.with_opacity(opacity, token)

    ft.colors = _ColorsCompat()  # type: ignore[attr-defined]


_ensure_colors_compat()


def _ensure_icons_compat() -> None:
    if hasattr(ft, "icons"):
        return

    class _IconsCompat:
        def __getattr__(self, name: str) -> str:
            attr = getattr(Icons, name)
            return attr.value if hasattr(attr, "value") else attr

    ft.icons = _IconsCompat()  # type: ignore[attr-defined]


_ensure_icons_compat()

<<<<<<< HEAD
try:
    from .state import AppState
    from .router import Router
except ImportError:
    AppState = None  # type: ignore[assignment]
    Router = None  # type: ignore[assignment]
=======
from .state import AppState
from .router import Router
>>>>>>> 5c98fc46a227f37a1229f81e2a08f6e4dd63f5ea

__all__ = ["AppState", "Router"]
