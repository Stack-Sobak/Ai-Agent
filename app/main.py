import asyncio

from fastapi import FastAPI

from .agent import BotInstance
from .schemas import ActivateRequest
from .websocket_client import BotWebSocketClient

app = FastAPI()
bot = BotInstance()
ws_client = None


@app.post("/activate")
async def activate(request: ActivateRequest):

    global ws_client

    bot.configure(
        name=request.name,
        description=request.description,
        personality=request.personality,
        participants=request.participants,
        bot_id=request.bot_id
    )

    ws_client = BotWebSocketClient(
        bot=bot,
        bot_id=bot.bot_id,
        bot_name=bot.bot_name
    )

    asyncio.create_task(ws_client.connect())

    print("Бот активирован. Информация: ", bot.get_info())

    return {"status": "activated"}


@app.post("/deactivate")
async def deactivate():
    bot.active = False
    return {"status": "deactivated"}