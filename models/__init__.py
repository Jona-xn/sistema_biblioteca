from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Optional

@dataclass(frozen=True)
class OperationResult:
    is_ok: bool
    error_message: Optional[str] = None

    @staticmethod
    def ok() -> "OperationResult":
        return OperationResult(True)

    @staticmethod
    def fail(message: str) -> "OperationResult":
        return OperationResult(False, message)

@dataclass(frozen=True)
class User:
    username: str
    full_name: Optional[str] = None

@dataclass
class Item:
    id: str
    name: str
    category: str
    quantity: int
    available_quantity: int
    status: str
    description: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class ItemCreateRequest:
    name: str
    category: str
    quantity: int
    description: Optional[str] = None
    status: str = "Disponible"

@dataclass
class LoanRequestItem:
    item: Item
    quantity: int


@dataclass
class LoanItem:
    item_id: str
    item_name: str
    category: str
    quantity: int


@dataclass
class Loan:
    id: str
    borrower_name: str
    loan_date: str
    loan_time: Optional[str]
    expected_return_date: str
    expected_return_time: Optional[str]
    status: str
    created_at: str
    items: List[LoanItem] = field(default_factory=list)

    @property
    def status_label(self) -> str:
        return "📋 Activo" if self.status == "active" else "✅ Devuelto"

    @property
    def status_color(self) -> str:
        return "#2E7D32" if self.status == "active" else "#607D8B"


@dataclass
class LoanReturn:
    id: str
    borrower_name: str
    loan_date: str
    loan_time: Optional[str]
    return_date: str
    return_time: Optional[str]
    items: List[LoanItem]
    categories: List[str]
    created_at: str

    @property
    def items_summary(self) -> str:
        return ", ".join(f"{item.item_name} ({item.quantity})" for item in self.items)

    @property
    def days_out(self) -> int:
        try:
            inicio = datetime.fromisoformat(self.loan_date)
            fin = datetime.fromisoformat(self.return_date)
            return max((fin - inicio).days, 0)
        except ValueError:
            return 0

    @property
    def status_label(self) -> str:
        return "⚠️ Tardío" if self.days_out > 15 else "✅ A tiempo"

    @property
    def status_color(self) -> str:
        return "#C62828" if self.days_out > 15 else "#2E7D32"


__all__ = [
    "OperationResult",
    "User",
    "Item",
    "ItemCreateRequest",
    "LoanRequestItem",
    "LoanItem",
    "Loan",
    "LoanReturn",
]
