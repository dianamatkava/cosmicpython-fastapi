from enum import StrEnum


class Queues(StrEnum):
    ORDER_CREATED_EVENT = "order_created_event"
    ORDER_LINE_ADDED_EVENT = "order_line_added_event"
    ORDER_LINE_REMOVED_EVENT = "order_line_removed_event"
    ORDER_STATUS_CHANGE_EVENT = "order_status_changed_event"
    ORDER_PAYED_EVENT = "order_payed_event"
    ORDER_SHIPPED_EVENT = "order_shipped_event"

    ALLOCATE_COMMAND = "allocate"
    DEALLOCATE_COMMAND = "deallocate"
    CHANGE_BATCH_QUANTITY_COMMAND = "change_batch_quantity"
    OUT_OF_STOCK_EVENT = "out_of_stock_event"
    BATCH_QUANTITY_CHANGED_EVENT = "batch_quantity_changed_event"


class LogCode(StrEnum):
    EVENT_FAILED = "EVENT_FAILED"
    COMMAND_FAILED = "COMMAND_FAILED"
