from dataclasses import dataclass
from datetime import date
from typing import List, Set, Optional


@dataclass(frozen=True)
class OrderLine:
    reference: str
    sku: str
    qty: int


@dataclass(frozen=True)
class Order:
    order_reference: str
    order_lines: List[OrderLine]


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date] = None):
        self.reference = ref
        self.sku = sku
        self.total_qty = qty
        self.eta = eta
        self._allocated_order_lines: Set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocated_order_lines.add(line)

    def deallocate(self, line: OrderLine):
        if self.can_deallocate(line):
            self._allocated_order_lines.remove(line)

    @property
    def available_quantity(self) -> int:
        return self.total_qty - self.allocated_quantity

    @property
    def allocated_quantity(self) -> int:
        return sum([x.qty for x in self._allocated_order_lines])

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def can_deallocate(self, line: OrderLine) -> bool:
        return line in self._allocated_order_lines


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    pass
