from datetime import date
from typing import Optional

from src.domain import batch_domain_model as domain
from src.tests.conftest import FakeRepository


class BatchFactory:

    def __init__(self, fake_repository: FakeRepository) -> None:
        self.fake_repository = fake_repository

    def for_batch(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        return self.fake_repository([domain.BatchModel(ref, sku, qty, eta)])

#
# def test_batch_allocates_when_has§_space(batch_service: BatchService, fake_uof: UnitOfWork, fake_session: FakeSession) -> None:
#     sku = "BLUE_VASE"
#     batch_1 = model.BatchModel('batch1', sku=sku, eta=datetime.strptime("2011-01-01", "%Y-%m-%d"), qty=10)
#     batch_2 = model.BatchModel('batch2', sku=sku, eta=datetime.strptime("2011-01-10", "%Y-%m-%d"), qty=10)
#
#     with fake_uof as uof:
#         uof.batch_repo.build([batch_1, batch_2])
#
#     order_line_1 = AllocationsAllocateIn(order_id="order_1", sku=sku, qty=10)
#     order_line_2 = AllocationsAllocateIn(order_id="order_2", sku=sku, qty=10)
#
#     res = batch_service.allocate(order_line_1)
#     assert res == batch_1.reference
#     assert batch_service.uof.session.committed is True
#
#     res = batch_service.allocate(order_line_2)
#     assert res == batch_2.reference
#
#     with pytest.raises(OutOfStock):
#         batch_service.allocate(order_line_2)