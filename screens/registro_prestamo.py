from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List, TYPE_CHECKING

import flet as ft

from models import Item, LoanRequestItem

from components.scroll_area import ScrollArea
from data.crud_inventario import listar_articulos_disponibles
from data.crud_prestamo import crear_prestamo

if TYPE_CHECKING:
    from app.state import AppState


class LoanSection(ft.Container):
    """Pantalla de registro de préstamos."""

    def __init__(self, state: "AppState") -> None:
        self.state = state
        self.available_items: List[Item] = []
        self.filtered_items: List[Item] = []
        self.selected_items: Dict[str, LoanRequestItem] = {}

        # Controles de formulario
        today = date.today()
        tomorrow = today + timedelta(days=1)

        self.borrower_field = ft.TextField(
            label="Nombre del Solicitante",
            hint_text="Ingrese el nombre completo",
            border_radius=12,
            prefix_icon=ft.Icons.PERSON,
            autofocus=True,
        )
        self.loan_date_field = ft.TextField(
            label="Fecha de Préstamo",
            value=today.strftime("%Y-%m-%d"),
            border_radius=12,
            prefix_icon=ft.Icons.EVENT,
        )
        self.loan_time_field = ft.TextField(
            label="Hora de Préstamo",
            value="10:00",
            border_radius=12,
            prefix_icon=ft.Icons.SCHEDULE,
        )
        self.return_date_field = ft.TextField(
            label="Fecha de Devolución",
            value=tomorrow.strftime("%Y-%m-%d"),
            border_radius=12,
            prefix_icon=ft.Icons.EVENT_AVAILABLE,
        )
        self.return_time_field = ft.TextField(
            label="Hora de Devolución",
            value="10:00",
            border_radius=12,
            prefix_icon=ft.Icons.SCHEDULE,
        )

        self.search_field = ft.TextField(
            label="Buscar artículos",
            hint_text="Buscar por nombre del artículo...",
            border_radius=12,
            prefix_icon=ft.Icons.SEARCH,
            on_change=self._on_filters_changed,
        )
        self.category_filter = ft.Dropdown(
            label="Categoría",
            options=[
                ft.dropdown.Option(""),
                ft.dropdown.Option("Literatura"),
                ft.dropdown.Option("Ciencias"),
                ft.dropdown.Option("Arte"),
                ft.dropdown.Option("Matemáticas"),
                ft.dropdown.Option("Tecnología"),
                ft.dropdown.Option("Geografía"),
            ],
            border_radius=12,
            value="",
            on_change=self._on_filters_changed,
        )

        self.available_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Artículo")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acción")),
            ],
            rows=[],
            column_spacing=20,
            heading_row_color=ft.colors.with_opacity(0.04, ft.colors.BLUE_200),
        )

        self.empty_state = ft.Container(
            width=float("inf"),
            padding=ft.padding.all(24),
            bgcolor=ft.colors.GREY_100,
            border_radius=16,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=64,
                        height=64,
                        bgcolor=ft.colors.WHITE,
                        border_radius=18,
                        alignment=ft.alignment.center,
                        content=ft.Text("📚", size=30),
                    ),
                    ft.Text(
                        "No hay artículos seleccionados",
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Busca y selecciona artículos de la lista",
                        size=12,
                        color=ft.colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        self.selected_items_column = ft.Column(controls=[self.empty_state], spacing=12, expand=True)

        self.confirm_button = ft.FilledButton(
            "Confirmar Préstamo",
            icon=ft.Icons.CHECK,
            height=48,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.colors.GREEN_600,
                    ft.ControlState.HOVERED: ft.colors.GREEN_700,
                },
                color={ft.ControlState.DEFAULT: ft.colors.WHITE},
                shape=ft.RoundedRectangleBorder(radius=14),
            ),
            on_click=self._handle_confirm_loan,
        )

        layout = self._build_layout()
        scrollable = ScrollArea(
            content=layout,
            padding=ft.padding.symmetric(horizontal=20, vertical=20),
        )
        super().__init__(expand=True, bgcolor=ft.colors.BLUE_GREY_50, content=scrollable)
        self._load_available_items()

    # ------------------------------------------------------------------ #
    # Construcción de la UI
    # ------------------------------------------------------------------ #
    def _build_layout(self) -> ft.Control:
        header = ft.Row(
            controls=[
                ft.Container(
                    width=48,
                    height=48,
                    bgcolor=ft.colors.BLUE_600,
                    border_radius=14,
                    alignment=ft.alignment.center,
                    content=ft.Text("📝", size=24),
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "Registrar Préstamo",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE_GREY_900,
                        ),
                        ft.Text(
                            "Completa la información del solicitante y selecciona los artículos a prestar.",
                            size=13,
                            color=ft.colors.GREY_600,
                        ),
                    ],
                    spacing=2,
                ),
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        borrower_card = ft.Container(
            bgcolor=ft.colors.WHITE,
            padding=24,
            border_radius=18,
            border=ft.border.all(1, ft.colors.with_opacity(0.08, ft.colors.BLUE_GREY)),
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=18,
                color=ft.colors.with_opacity(0.12, ft.colors.BLUE_GREY_900),
            ),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=40,
                                height=40,
                                bgcolor=ft.colors.BLUE_100,
                                border_radius=12,
                                alignment=ft.alignment.center,
                                content=ft.Text("👤"),
                            ),
                            ft.Text(
                                "Información del Solicitante",
                                size=18,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.BLUE_GREY_900,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Column(controls=[self.borrower_field], col={"xs": 12}),
                            ft.Column(controls=[self.loan_date_field], col={"xs": 6, "md": 3}),
                            ft.Column(controls=[self.loan_time_field], col={"xs": 6, "md": 3}),
                            ft.Column(controls=[self.return_date_field], col={"xs": 6, "md": 3}),
                            ft.Column(controls=[self.return_time_field], col={"xs": 6, "md": 3}),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=16,
            ),
        )

        filters_row = ft.ResponsiveRow(
            controls=[
                ft.Container(content=self.search_field, col={"xs": 12, "md": 8}),
                ft.Container(content=self.category_filter, col={"xs": 12, "md": 4}),
            ],
            spacing=12,
            run_spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )

        available_card = ft.Container(
            bgcolor=ft.colors.WHITE,
            padding=24,
            border_radius=18,
            border=ft.border.all(1, ft.colors.with_opacity(0.08, ft.colors.BLUE_GREY)),
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=18,
                color=ft.colors.with_opacity(0.12, ft.colors.BLUE_GREY_900),
            ),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=40,
                                height=40,
                                bgcolor=ft.colors.GREEN_100,
                                border_radius=12,
                                alignment=ft.alignment.center,
                                content=ft.Text("📚"),
                            ),
                            ft.Text(
                                "Seleccionar Artículos",
                                size=18,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.BLUE_GREY_900,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    filters_row,
                    ft.Divider(height=16, color=ft.colors.TRANSPARENT),
                    ft.Container(
                        expand=True,
                        height=360,
                        border_radius=12,
                        bgcolor=ft.colors.BLUE_GREY_50,
                        content=ft.ListView(controls=[self.available_table], expand=True),
                    ),
                ],
                spacing=16,
            ),
        )

        left_column = ft.Column(
            controls=[header, borrower_card, available_card],
            spacing=20,
            expand=True,
        )

        selected_panel = ft.Container(
            bgcolor=ft.colors.WHITE,
            padding=24,
            border_radius=18,
            border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY)),
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=18,
                color=ft.colors.with_opacity(0.12, ft.colors.BLUE_GREY_900),
            ),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=40,
                                height=40,
                                bgcolor=ft.colors.ORANGE_100,
                                border_radius=12,
                                alignment=ft.alignment.center,
                                content=ft.Text("📋"),
                            ),
                            ft.Text(
                                "Artículos seleccionados",
                                size=18,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.BLUE_GREY_900,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=8, color=ft.colors.TRANSPARENT),
                    ft.Container(
                        expand=True,
                        height=360,
                        content=ft.ListView(controls=[self.selected_items_column], expand=True),
                    ),
                    self.confirm_button,
                ],
                spacing=16,
                expand=True,
            ),
        )

        left_container = ft.Container(content=left_column)
        left_container.col = {"xs": 12, "lg": 7}
        selected_panel.col = {"xs": 12, "lg": 5}

        return ft.ResponsiveRow(
            controls=[left_container, selected_panel],
            spacing=20,
            run_spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    # ------------------------------------------------------------------ #
    # Gestión de datos
    # ------------------------------------------------------------------ #
    def _load_available_items(self) -> None:
        self.available_items = listar_articulos_disponibles()
        self._apply_filters()

    def _apply_filters(self) -> None:
        search = (self.search_field.value or "").lower()
        category = self.category_filter.value or ""

        self.filtered_items = [
            item
            for item in self.available_items
            if (not search or search in item.name.lower())
            and (not category or item.category == category)
        ]
        self._render_available_table()

    def _render_available_table(self) -> None:
        def build_row(item: Item) -> ft.DataRow:
            return ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Column(
                            controls=[
                                ft.Text(item.name, weight=ft.FontWeight.W_600),
                                ft.Text(
                                    item.description or "Sin descripción",
                                    size=12,
                                    color=ft.colors.GREY_600,
                                ),
                            ],
                            spacing=2,
                        )
                    ),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.Text(item.category_icon),
                                ft.Text(item.category),
                            ],
                            spacing=6,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            "Disponible" if item.available_quantity > 0 else "Agotado",
                            color=ft.colors.GREEN_600
                            if item.available_quantity > 0
                            else ft.colors.RED_400,
                        )
                    ),
                    ft.DataCell(
                        ft.OutlinedButton(
                            "Agregar",
                            icon=ft.Icons.ADD,
                            on_click=lambda _, i=item: self._add_item(i),
                        )
                    ),
                ]
            )

        self.available_table.rows = [build_row(item) for item in self.filtered_items]
        self._safe_update(self.available_table)

    def _render_selected_items(self) -> None:
        if not self.selected_items:
            self.selected_items_column.controls = [self.empty_state]
            self._safe_update(self.selected_items_column)
            return

        items_controls: List[ft.Control] = []
        for request_item in self.selected_items.values():
            def make_on_add(item_id: str):
                return lambda _: self._change_quantity(item_id, 1)

            def make_on_subtract(item_id: str):
                return lambda _: self._change_quantity(item_id, -1)

            items_controls.append(
                ft.Container(
                    border_radius=14,
                    border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY)),
                    padding=16,
                    bgcolor=ft.colors.WHITE,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        width=32,
                                        height=32,
                                        bgcolor=ft.colors.ORANGE_100,
                                        border_radius=10,
                                        alignment=ft.alignment.center,
                                        content=ft.Text("📚"),
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(request_item.item.name, weight=ft.FontWeight.W_600),
                                            ft.Text(
                                                request_item.item.category,
                                                size=12,
                                                color=ft.colors.GREY_600,
                                            ),
                                        ],
                                        spacing=2,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.colors.RED_400,
                                        tooltip="Quitar artículo",
                                        on_click=lambda _, iid=request_item.item.id: self._remove_item(iid),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Cantidad", size=12, color=ft.colors.GREY_600),
                                    ft.IconButton(icon=ft.Icons.REMOVE, on_click=make_on_subtract(request_item.item.id)),
                                    ft.Text(str(request_item.quantity)),
                                    ft.IconButton(icon=ft.Icons.ADD, on_click=make_on_add(request_item.item.id)),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                )
            )

        self.selected_items_column.controls = items_controls
        self._safe_update(self.selected_items_column)

    # ------------------------------------------------------------------ #
    # Eventos
    # ------------------------------------------------------------------ #
    def _on_filters_changed(self, _: ft.ControlEvent) -> None:
        self._apply_filters()

    def _add_item(self, item: Item) -> None:
        if item.id not in self.selected_items:
            self.selected_items[item.id] = LoanRequestItem(item=item, quantity=1)
        else:
            self.selected_items[item.id].quantity += 1
        self._render_selected_items()

    def _remove_item(self, item_id: str) -> None:
        if item_id in self.selected_items:
            del self.selected_items[item_id]
            self._render_selected_items()

    def _change_quantity(self, item_id: str, delta: int) -> None:
        if item_id not in self.selected_items:
            return
        new_quantity = self.selected_items[item_id].quantity + delta
        if new_quantity <= 0:
            self._remove_item(item_id)
        else:
            self.selected_items[item_id].quantity = new_quantity
            self._render_selected_items()

    def _handle_confirm_loan(self, _: ft.ControlEvent) -> None:
        if not self.selected_items:
            self.state.notify("Selecciona al menos un artículo.", kind="error")
            return

        borrower = (self.borrower_field.value or "").strip()
        if not borrower:
            self.state.notify("Ingresa el nombre del solicitante.", kind="error")
            return

        result = crear_prestamo(
            solicitante=borrower,
            fecha_prestamo=self.loan_date_field.value or "",
            hora_prestamo=self.loan_time_field.value or "",
            fecha_devolucion=self.return_date_field.value or "",
            hora_devolucion=self.return_time_field.value or "",
            articulos=list(self.selected_items.values()),
        )

        if not result.is_ok:
            self.state.notify(result.error_message or "No se pudo registrar el préstamo.", kind="error")
            return

        self.state.notify("Préstamo registrado correctamente.")
        self.selected_items.clear()
        self._render_selected_items()
        self._load_available_items()

    def _safe_update(self, control: ft.Control) -> None:
        if getattr(control, "page", None):
            control.update()

