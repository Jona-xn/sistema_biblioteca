from __future__ import annotations

from datetime import date, datetime, time
from typing import Callable, Optional

import flet as ft


class _BasePickerField(ft.Container):
    """Contenedor común para campos con selector emergente."""

    def __init__(
        self,
        *,
        label: str,
        icon: str,
        placeholder: str,
        initial_value: str = "",
        on_change: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._label = label
        self._icon = icon
        self._placeholder = placeholder
        self._on_change = on_change
        self._value = initial_value

        self._value_text = ft.Text(
            self._value or self._placeholder,
            color=ft.colors.BLUE_GREY_900 if self._value else ft.colors.GREY_500,
            no_wrap=True,
        )

        content = ft.Column(
            spacing=4,
            controls=[
                ft.Text(
                    self._label,
                    size=12,
                    color=ft.colors.GREY_600,
                ),
                ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(self._icon, size=20, color=ft.colors.GREY_800),
                        ft.Container(expand=True, content=self._value_text),
                    ],
                ),
            ],
        )

        super().__init__(
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=16,
            padding=ft.padding.symmetric(12, 16),
            content=content,
        )

        self.on_click = self._handle_click

    @property
    def value(self) -> str:
        return self._value

    def set_value(self, value: str) -> None:
        self._value = value
        self._value_text.value = value or self._placeholder
        self._value_text.color = (
            ft.colors.BLUE_GREY_900 if value else ft.colors.GREY_500
        )
        if self._on_change:
            self._on_change(value)
        self.update()

    def _handle_click(self, _: ft.TapEvent) -> None:
        if self.page:
            self._open_picker()

    def _open_picker(self) -> None:  # pragma: no cover - definido en subclases
        raise NotImplementedError


class DateInput(_BasePickerField):
    """Campo reutilizable que usa el DatePicker nativo de Flet (estilo Windows)."""

    def __init__(
        self,
        *,
        label: str = "Fecha",
        icon: str = ft.Icons.EVENT,
        initial_date: Optional[date] = None,
        placeholder: str = "Seleccionar fecha",
        first_date: Optional[date] = None,
        last_date: Optional[date] = None,
        on_change: Optional[Callable[[str], None]] = None,
        date_format: str = "%Y-%m-%d",
    ) -> None:
        self._date_format = date_format
        today = date.today()
        self._current_date = initial_date or today
        self._first_date = first_date or date(today.year - 5, 1, 1)
        self._last_date = last_date or date(today.year + 5, 12, 31)

        if self._current_date < self._first_date:
            self._current_date = self._first_date
        if self._current_date > self._last_date:
            self._current_date = self._last_date

        super().__init__(
            label=label,
            icon=icon,
            placeholder=placeholder,
            initial_value=self._current_date.strftime(self._date_format),
            on_change=on_change,
        )

        self._picker = ft.DatePicker(
            value=self._current_date,
            first_date=self._first_date,
            last_date=self._last_date,
            on_change=self._handle_picker_change,
            on_dismiss=self._handle_dismiss,
        )

    def set_value(self, value: str) -> None:  # type: ignore[override]
        parsed = value
        if value:
            try:
                parsed_date = datetime.strptime(value, self._date_format).date()
            except ValueError:
                parsed_date = None
            if parsed_date:
                self._current_date = parsed_date
                self._picker.value = parsed_date
                parsed = parsed_date.strftime(self._date_format)
        super().set_value(parsed)

    def _ensure_in_overlay(self) -> None:
        if not self.page:
            return
        if self._picker not in self.page.overlay:
            self.page.overlay.append(self._picker)

    def _open_picker(self) -> None:
        if not self.page:
            return
        self._ensure_in_overlay()
        self._picker.open = True
        self.page.update()

    def _handle_picker_change(self, e: ft.DatePickerChangeEvent) -> None:
        if not e.data:
            return
        selected = datetime.fromisoformat(e.data).date()
        self._current_date = selected
        super().set_value(selected.strftime(self._date_format))

    def _handle_dismiss(self, _: ft.ControlEvent) -> None:
        if self.page:
            self.page.update()


class TimeInput(_BasePickerField):
    """Campo reutilizable que usa el TimePicker nativo de Flet."""

    def __init__(
        self,
        *,
        label: str = "Hora",
        icon: str = ft.Icons.SCHEDULE,
        initial_time: Optional[time] = None,
        placeholder: str = "Seleccionar hora",
        on_change: Optional[Callable[[str], None]] = None,
        time_format: str = "%H:%M",
        step_minutes: int = 5,
    ) -> None:
        self._time_format = time_format
        self._current_time = initial_time or time(10, 0)
        super().__init__(
            label=label,
            icon=icon,
            placeholder=placeholder,
            initial_value=self._current_time.strftime(self._time_format),
            on_change=on_change,
        )

        self._picker = ft.TimePicker(
            value=self._current_time,
            on_change=self._handle_picker_change,
            on_dismiss=self._handle_dismiss,
            help_text="Seleccionar hora",
            )

    def set_value(self, value: str) -> None:  # type: ignore[override]
        parsed = value
        if value:
            parsed_time: Optional[time]
            try:
                parsed_time = datetime.strptime(value, self._time_format).time()
            except ValueError:
                try:
                    parsed_time = time.fromisoformat(value)
                except ValueError:
                    parsed_time = None
            if parsed_time:
                self._current_time = parsed_time
                self._picker.value = parsed_time
                parsed = parsed_time.strftime(self._time_format)
        super().set_value(parsed)

    def _ensure_in_overlay(self) -> None:
        if not self.page:
            return
        if self._picker not in self.page.overlay:
            self.page.overlay.append(self._picker)

    def _open_picker(self) -> None:
        if not self.page:
            return
        self._ensure_in_overlay()
        self._picker.open = True
        self.page.update()

    def _handle_picker_change(self, e: ft.TimePickerChangeEvent) -> None:
        if not e.data:
            return
        parts = [int(p) for p in e.data.split(':')]
        while len(parts) < 3:
            parts.append(0)
        selected = time(parts[0], parts[1], parts[2])
        self._current_time = selected
        super().set_value(selected.strftime(self._time_format))

    def _handle_dismiss(self, _: ft.ControlEvent) -> None:
        if self.page:
            self.page.update()


__all__ = ["DateInput", "TimeInput"]


