from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List

import flet as ft


@dataclass(frozen=True)
class SidebarEntry:
    key: str
    icon: str
    label: str


class Sidebar(ft.Container):
    """Barra lateral reutilizable para la app."""

    def __init__(self, *, on_change: Callable[[str], None], active: str = "loan") -> None:
        self.on_change = on_change
        self.active_key = active

        self.entries: List[SidebarEntry] = [
            SidebarEntry("loan", "📝", "Registrar Préstamo"),
            SidebarEntry("inventory", "📦", "Inventario"),
            SidebarEntry("loans", "📋", "Préstamos"),
            SidebarEntry("returns", "↩️", "Devoluciones"),
        ]
        self.buttons: List[ft.Container] = []

        super().__init__(
            width=260,
            bgcolor=ft.colors.BLUE_900,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.BLUE_900, ft.colors.INDIGO_900],
            ),
        )
        self._build()

    def _build(self) -> None:
        header = ft.Container(
            padding=24,
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.with_opacity(0.1, ft.colors.WHITE))),
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=40,
                        height=40,
                        bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE),
                        border_radius=12,
                        alignment=ft.alignment.center,
                        content=ft.Text("📚", size=20),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Biblioteca Central", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text("Panel de control", size=12, color=ft.colors.with_opacity(0.8, ft.colors.WHITE)),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        items_column = ft.Column(spacing=8)
        self.buttons = []
        for entry in self.entries:
            button = self._build_button(entry)
            self.buttons.append(button)
            items_column.controls.append(button)

        logout_button = ft.TextButton(
            "Cerrar sesión",
            icon=ft.icons.LOGOUT,
            style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: ft.colors.WHITE}),
            on_click=lambda _: self.on_change("logout"),
        )

        footer = ft.Container(
            padding=24,
            border=ft.border.only(top=ft.border.BorderSide(1, ft.colors.with_opacity(0.1, ft.colors.WHITE))),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE),
                                content=ft.Text("👤"),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Administrador", color=ft.colors.WHITE, weight=ft.FontWeight.W_600),
                                    ft.Text("Sistema activo", size=12, color=ft.colors.with_opacity(0.7, ft.colors.WHITE)),
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    logout_button,
                ],
                spacing=16,
            ),
        )

        self.content = ft.Column(
            controls=[header, ft.Container(padding=24, content=items_column), footer],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_button(self, entry: SidebarEntry) -> ft.Container:
        is_active = entry.key == self.active_key

        def handle_click(_: ft.ControlEvent) -> None:
            if entry.key == "logout":
                self.on_change("logout")
            else:
                self.set_active(entry.key)
                self.on_change(entry.key)

        return ft.Container(
            on_click=handle_click,
            padding=16,
            border_radius=14,
            bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE) if is_active else None,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=32,
                        height=32,
                        bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE) if is_active else ft.colors.with_opacity(0.1, ft.colors.WHITE),
                        border_radius=10,
                        alignment=ft.alignment.center,
                        content=ft.Text(entry.icon, size=18),
                    ),
                    ft.Text(
                        entry.label,
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL,
                    ),
                ],
                spacing=12,
            ),
        )

    def set_active(self, key: str) -> None:
        self.active_key = key
        for entry, button in zip(self.entries, self.buttons):
            is_active = entry.key == key
            button.bgcolor = ft.colors.with_opacity(0.2, ft.colors.WHITE) if is_active else None
            icon_container = button.content.controls[0]
            icon_container.bgcolor = (
                ft.colors.with_opacity(0.2, ft.colors.WHITE)
                if is_active
                else ft.colors.with_opacity(0.1, ft.colors.WHITE)
            )
            label = button.content.controls[1]
            label.weight = ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL
        if getattr(self, "page", None):
            self.update()
