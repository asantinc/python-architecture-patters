import pytest

from model import OrderLine, Batch


def make_batch_and_line(sku, batch_qty, line_qty):
    return (Batch("batch-001", sku, batch_qty), OrderLine("order-001", sku, line_qty))


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
    pytest.fail("todo")


# def test_prefers_warehouse_batches_to_shipments():
#     pytest.fail("todo")
#
#
# def test_prefers_earlier_batches():
#     pytest.fail("todo")
