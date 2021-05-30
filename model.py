from dataclasses import dataclass
from typing import List


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
    def __init__(self, ref: str, sku: str, qty: int):
        self.reference = ref
        self.sku = sku
        self.available_quantity = qty

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            return
        self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku != line.sku or self.available_quantity < line.qty