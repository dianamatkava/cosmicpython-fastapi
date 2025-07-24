from datetime import date


class InventoryBatchModel:
    reference: str
    sku: str
    eta: date | None
    qty: int  # initial quantity

    def __init__(self, reference, sku, eta, qty):
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self.qty = qty
