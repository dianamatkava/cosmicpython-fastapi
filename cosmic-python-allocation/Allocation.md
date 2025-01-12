Some Notes on Allocation

A product is identified by a SKU, pronounced "skew," which is short for stock-keeping unit. Customers place orders. An order is identified by an order reference and comprises multiple order lines, where each line has a SKU and a quantity. For example:

10 units of RED-CHAIR

1 unit of TASTELESS-LAMP

The purchasing department orders small batches of stock. A batch of stock has a unique ID called a reference, a SKU, and a quantity.

We need to allocate order lines to batches. When we’ve allocated an order line to a batch, we will send stock from that specific batch to the customer’s delivery address. When we allocate x units of stock to a batch, the available quantity is reduced by x. For example:

We have a batch of 20 SMALL-TABLE, and we allocate an order line for 2 SMALL-TABLE.

The batch should have 18 SMALL-TABLE remaining.

We can’t allocate to a batch if the available quantity is less than the quantity of the order line. For example:

We have a batch of 1 BLUE-CUSHION, and an order line for 2 BLUE-CUSHION.

We should not be able to allocate the line to the batch.

We can’t allocate the same line twice. For example:

We have a batch of 10 BLUE-VASE, and we allocate an order line for 2 BLUE-VASE.

If we allocate the order line again to the same batch, the batch should still have an available quantity of 8.

Batches have an ETA if they are currently shipping, or they may be in warehouse stock. We allocate to warehouse stock in preference to shipment batches. We allocate to shipment batches in order of which has the earliest ETA.