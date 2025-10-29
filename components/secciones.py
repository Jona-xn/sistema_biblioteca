from __future__ import annotations

from typing import Iterable

import flet as ft


def crear_tarjeta_contenido(
    *,
    controles: Iterable[ft.Control],
    padding: int = 32,
    radio: int = 20,
) -> ft.Container:
    """Tarjeta blanca reutilizable para formularios y paneles."""
    return ft.Container(
        padding=ft.padding.all(padding),
        bgcolor=ft.colors.WHITE,
        border_radius=radio,
        shadow=ft.BoxShadow(
            spread_radius=-2,
            blur_radius=20,
            color=ft.colors.with_opacity(0.25, ft.colors.BLUE_GREY_900),
        ),
        content=ft.Column(
            controls=list(controles),
            spacing=16,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )


def crear_aviso_informativo(
    *,
    icono: str,
    titulo: str,
    descripcion: str,
) -> ft.Container:
    """Caja informativa reutilizable para mensajes contextuales."""
    return ft.Container(
        bgcolor=ft.colors.BLUE_50,
        border_radius=12,
        padding=16,
        border=ft.border.all(1, ft.colors.BLUE_100),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(icono, size=20),
                        ft.Text(
                            titulo,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=ft.colors.BLUE_600,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(descripcion, size=12, color=ft.colors.BLUE_GREY_500),
            ],
            spacing=8,
        ),
    )


def crear_panel_destacado(
    *,
    titulo: str,
    icono: str,
    caracteristicas: Iterable[tuple[str, str]],
) -> ft.Container:
    """Panel decorativo con gradiente y listado de características."""
    elementos = [
        ft.Container(
            width=96,
            height=96,
            bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE),
            border_radius=28,
            alignment=ft.alignment.center,
            content=ft.Text(icono, size=48),
        ),
        ft.Text(
            titulo,
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Column(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.with_opacity(0.18, ft.colors.WHITE),
                    border_radius=16,
                    padding=ft.padding.symmetric(vertical=12, horizontal=18),
                    content=ft.Row(
                        controls=[ft.Text(simbolo, size=20), ft.Text(texto, size=16)],
                        spacing=12,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                )
                for simbolo, texto in caracteristicas
            ],
            spacing=12,
        ),
    ]

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.colors.BLUE_700, ft.colors.INDIGO, ft.colors.INDIGO_900],
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(48),
        content=ft.Column(
            controls=elementos,
            spacing=24,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
