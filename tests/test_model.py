from datetime import datetime, date, timedelta

import pytest

from model import OrderLine, Batch, allocate


def make_batch_and_line(sku, batch_qty, line_qty, line_sku=None):
    line_sku = line_sku if line_sku else sku
    return (
        Batch("batch-001", sku, batch_qty),
        OrderLine("order-001", line_sku, line_qty),
    )


def test_allocating_to_batch_reduces_the_availability_quantity():
    batch = Batch("batch-001", "SMALL_TABLE", qty=20)
    line = OrderLine(reference="order-red", sku="SMALL_TABLE", qty=2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_line("CHAIR", 10, 5)

    batch.allocate(line)

    assert batch.available_quantity == 5


def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_line("CHAIR", 5, 10)

    batch.allocate(line)

    assert batch.available_quantity == 5


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("CHAIR", 5, 5)

    batch.allocate(line)

    assert batch.available_quantity == 0


def test_cannot_allocate_if_skus_do_not_match():
    batch, line = make_batch_and_line("CHAIR", 5, 5, line_sku="TABLE")

    batch.allocate(line)

    assert batch.available_quantity == 5


def test_cannot_deallocate_unallocated_lines():
    batch, unallocated_line = make_batch_and_line("CHAIR", 5, 5)

    batch.deallocate(unallocated_line)

    assert batch.available_quantity == 5


def test_can_deallocate_allocated_lines():
    batch, line = make_batch_and_line("CHAIR", 5, 5)

    batch.allocate(line)
    assert batch.available_quantity == 0

    batch.deallocate(line)
    assert batch.available_quantity == 5


def test_cannot_allocate_repeatedly():
    batch, line = make_batch_and_line("CHAIR", 10, 5)

    batch.allocate(line)
    assert batch.available_quantity == 5
    batch.allocate(line)
    assert batch.available_quantity == 5


def test_prefers_warehouse_batches_to_shipments():
    in_stock_batch = Batch(ref="ref", qty=10, sku="sku", eta=None)
    shipment_batch = Batch(ref="ref", qty=10, sku="sku", eta=date.today())
    line = OrderLine(reference="xyz", sku="sku", qty=10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 0
    assert shipment_batch.available_quantity == 10


def test_prefers_earlier_batches():
    early_batch = Batch(ref="ref", qty=10, sku="sku", eta=date.today())
    later_batch = Batch(
        ref="ref", qty=10, sku="sku", eta=date.today() + timedelta(days=1)
    )
    line = OrderLine(reference="xyz", sku="sku", qty=10)

    allocate(line, [early_batch, later_batch])

    assert early_batch.available_quantity == 0
    assert later_batch.available_quantity == 10
