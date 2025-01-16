from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

from page import html


router = APIRouter(prefix='/websocket')


@router.get('/')
async def websocket_root():
    return HTMLResponse(html)


@router.websocket("/subscribe")
async def websocket_subscribe(websocket: WebSocket):
    pass

