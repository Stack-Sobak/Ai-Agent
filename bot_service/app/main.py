from fastapi import FastAPI

from agent import BotInstance
from schemas import ActivateRequest
from websocket_client import BotWebSocketClient
import asyncio

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
        backend_url="ws://localhost:8080",
        bot_id=bot.bot_id,
        bot_name=bot.bot_name
    )

    asyncio.create_task(ws_client.connect())

    return {"status": "activated"}


@app.post("/deactivate")
async def deactivate():
    bot.active = False
    return {"status": "deactivated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
