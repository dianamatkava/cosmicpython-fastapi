from fastapi import FastAPI

from src.conf import create_db_and_tables
from src.routes.websocket import router as websocket_router

app = FastAPI()
app.include_router(websocket_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# @app.get("/")
# def home(session: Annotated[Any, Depends(get_session)]):
#     products = session.query(Product).all()
#     print(products)
#     return 201
