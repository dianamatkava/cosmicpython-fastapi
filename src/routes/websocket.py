import abc
from typing import Annotated

from fastapi import APIRouter, WebSocket, Query, WebSocketException, Depends, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status

from src.routes.page import html

router = APIRouter(prefix='/websocket')


@router.get('/')
async def websocket_root():
    return HTMLResponse(html)


async def get_token(
    token: Annotated[str | None, Query()] = None,
):
    if token != 'secret':
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token


async def get_user(user_id: str) -> str:
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return "🙍🏼‍♀️" + user_id


class AbstractWebSocketManager(abc.ABC):
    async def connect(self, websocket: WebSocket) -> None:
        ...

    def disconnect(self, websocket: WebSocket) -> None:
        ...

    async def send(self, message: str, websocket: WebSocket) -> None:
        ...

    async def broadcast(self, message: str, websocket: WebSocket):
        ...


class WebSocketManager(AbstractWebSocketManager):
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.remove(websocket)

    async def send(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket):
        for connection in self.connections:
            if connection is not websocket:
                await connection.send_text(message)


websocket_manager = WebSocketManager()


@router.websocket("/chat/{user_id}")
async def websocket_chat(
    *,
    websocket: WebSocket,
    # _: Annotated[str, Depends(get_token)],
    sender: Annotated[str, Depends(get_user)],
    # websocket_manager: Annotated[WebSocketManager, Depends(get_websocket_manager)]
):
    try:
        await websocket_manager.connect(websocket)
        while True:
            data = await websocket.receive_text()
            await websocket_manager.send(f"You wrote:\n {data}\n\n", websocket)
            await websocket_manager.broadcast(f"{sender}:\n {data}\n\n", websocket)
    except Exception:
        websocket_manager.disconnect(websocket)
        await websocket_manager.broadcast(f"User {sender} left group", websocket)

