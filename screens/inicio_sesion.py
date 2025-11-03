from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import flet as ft

from components.botones import crear_boton_principal
from components.campos import crear_campo_texto
from components.secciones import (
    crear_aviso_informativo,
    crear_panel_destacado,
    crear_tarjeta_contenido,
)
from components.validaciones import validar_credenciales
from data.crud_admin import validar_credenciales_admin

if TYPE_CHECKING:
    from app.router import Router
    from app.state import AppState


def construir_vista_inicio_sesion(enrutador: "Router", estado: "AppState") -> ft.View:
    """Genera la vista de autenticación principal."""

    campo_usuario = crear_campo_texto(
        "Usuario",
        "Ingresa tu usuario",
        ft.Icons.PERSON,
        autofoco=True,
    )
    campo_contrasena = crear_campo_texto(
        "Contraseña",
        "Ingresa tu contraseña",
        ft.Icons.LOCK,
        es_password=True,
    )

    def manejar_envio(_: ft.ControlEvent) -> None:
        if getattr(estado, "es_vista_previa", False):
            if hasattr(estado, "notify"):
                estado.notify("Vista previa: la acción del botón está deshabilitada.", kind="info")
            return

        usuario = (campo_usuario.value or "").strip()
        contrasena = campo_contrasena.value or ""

        es_valido, errores = validar_credenciales(usuario, contrasena)
        if not es_valido:
            estado.notify(errores[0], kind="error")
            return

        registro = validar_credenciales_admin(usuario, contrasena)
        if registro is None:
            estado.notify("Credenciales incorrectas.", kind="error")
            return

        estado.set_session(registro["usuario"], registro.get("usuario"))
        estado.notify("Bienvenido al sistema bibliotecario.", kind="success")
        enrutador.replace("/dashboard")

    def manejar_recuperacion(_: ft.ControlEvent) -> None:
        script_path = Path(__file__).resolve().parents[1] / "scripts" / "mostrar_credenciales.py"
        if not script_path.exists():
            estado.notify("El script de recuperación no está disponible.", kind="error")
            return

        try:
            if sys.platform.startswith("win"):
                flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
                subprocess.Popen([sys.executable, str(script_path)], creationflags=flags)
            else:
                subprocess.Popen([sys.executable, str(script_path)])
        except OSError as exc:
            estado.notify(f"No se pudo ejecutar el script: {exc}", kind="error")

    boton_acceder = crear_boton_principal(
        "Iniciar sesión",
        ft.Icons.LOGIN,
        evento=manejar_envio,
    )

    tarjeta_formulario = crear_tarjeta_contenido(
        controles=[
            _construir_encabezado_tarjeta(),
            ft.Divider(height=32, color=ft.colors.TRANSPARENT),
            campo_usuario,
            campo_contrasena,
            ft.Divider(height=16, color=ft.colors.TRANSPARENT),
            boton_acceder,
            ft.TextButton(
                "Recuperar contraseña",
                icon=ft.Icons.KEY,
                style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: ft.colors.BLUE_600}),
                on_click=manejar_recuperacion,
            ),
            crear_aviso_informativo(
                icono="💡",
                titulo="Credenciales de demostración",
                descripcion="Usuario: admin\nContraseña: admin123",
            ),
        ]
    )

    panel_formulario = ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=24),
        alignment=ft.alignment.center,
        content=ft.Column(
            width=420,
            controls=[tarjeta_formulario],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    panel_destacado = crear_panel_destacado(
        titulo="Sistema de Gestión Bibliotecaria",
        icono="📚",
        caracteristicas=_obtener_caracteristicas_destacadas(),
    )

    contenedor_principal = ft.Row(
        controls=[panel_formulario, panel_destacado],
        spacing=0,
        expand=True,
    )

    return ft.View(
        route="/",
        controls=[contenedor_principal],
        bgcolor=ft.colors.BLUE_GREY_50,
        padding=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )


def _construir_encabezado_tarjeta() -> ft.Column:
    """Cabecera reutilizable para tarjetas de autenticación."""
    return ft.Column(
        controls=[
            ft.Container(
                width=64,
                height=64,
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_900),
                border_radius=18,
                alignment=ft.alignment.center,
                content=ft.Text("📚", size=32),
            ),
            ft.Text(
                "Biblioteca Central",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_900,
            ),
            ft.Text(
                "Iniciar Sesión",
                size=16,
                color=ft.colors.BLUE_GREY_600,
            ),
        ],
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _obtener_caracteristicas_destacadas() -> list[tuple[str, str]]:
    """Listado de características visibles en el panel informativo."""
    return [
        ("📦", "Gestión de inventario"),
        ("📋", "Control de préstamos"),
        ("↩️", "Seguimiento de devoluciones"),
        ("📊", "Reportes automáticos"),
    ]
