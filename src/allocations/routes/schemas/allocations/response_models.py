from typing import List

from pydantic import BaseModel, RootModel

from src.allocations.services.schemas import BatchSchemaDTO


class BatchesListResponseModel(RootModel[List[BatchSchemaDTO]]):
    """Model represent list of batches."""


class AllocationsAllocateResponseModel(BaseModel):
    reference: str
