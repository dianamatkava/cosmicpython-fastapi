from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import clear_mappers
from starlette import status

from src.adapters.orm_mappers import start_mappers
from src.allocations.routes.v1.allocations import router as allocations_router
from src.orders.routes.order_line import router as order_line_router
from src.inventory.routes.batchs import router as batch_router
from src.inventory.routes.product import router as product_router

app = FastAPI()
router = APIRouter(prefix="", tags=["main"])

# TODO: Add Auth on OpenAPI
app.include_router(allocations_router)
app.include_router(order_line_router)
app.include_router(batch_router)
app.include_router(product_router)


@router.get("/healthcheck", response_model=None, status_code=status.HTTP_200_OK)
def get_app_healthcheck():
    """Router to get all healthcheck."""


@app.on_event("startup")
def on_startup():
    clear_mappers()
    start_mappers()


@app.on_event("shutdown")
def on_shutdown():
    clear_mappers()
