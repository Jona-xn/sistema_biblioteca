"""Funciones de validación reutilizables para formularios."""

from __future__ import annotations

import re
from typing import Optional


def es_no_vacio(valor: Optional[str]) -> bool:
    """Indica si el valor contiene texto distinto de espacios."""
    return bool(valor and valor.strip())


def es_solo_letras(valor: str) -> bool:
    """Valida que el texto contenga únicamente letras y espacios."""
    return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñüÜ\s]+", valor or ""))


def es_alfa_numerico(valor: str) -> bool:
    """Comprueba que el texto posea letras, números o guiones bajos."""
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", valor or ""))


def es_entero(valor: str) -> bool:
    """Determina si el valor es un entero (positivo o negativo)."""
    return bool(re.fullmatch(r"-?\d+", valor or ""))


def longitud_entre(valor: str, minimo: int, maximo: Optional[int] = None) -> bool:
    """Valida que la longitud del texto esté entre los límites dados."""
    if valor is None:
        return False
    longitud = len(valor)
    if longitud < minimo:
        return False
    if maximo is not None and longitud > maximo:
        return False
    return True


def validar_credenciales(usuario: str, contrasena: str) -> tuple[bool, list[str]]:
    """Comprueba reglas básicas para credenciales de inicio de sesión."""
    errores: list[str] = []

    if not es_no_vacio(usuario):
        errores.append("Debe ingresar un nombre de usuario.")
    elif not es_alfa_numerico(usuario):
        errores.append("El nombre de usuario solo puede contener letras, números o guiones bajos.")

    if not es_no_vacio(contrasena):
        errores.append("Debe ingresar una contraseña.")
    elif not longitud_entre(contrasena, minimo=4):
        errores.append("La contraseña debe tener al menos 4 caracteres.")

    return (len(errores) == 0, errores)


__all__ = [
    "es_no_vacio",
    "es_solo_letras",
    "es_alfa_numerico",
    "es_entero",
    "longitud_entre",
    "validar_credenciales",
]
