from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import List

from agent import BotInstance
from llm_client import ask_llm, summarize_text

app = FastAPI()
bot = BotInstance()

class CreateBotRequest(BaseModel):
    name: str
    description: str
    personality: str
    participants: List[str]

class UpdateParticipantsRequest(BaseModel):
    participants: List[str]


@app.post("/activate")
async def activate_bot(request: CreateBotRequest):
    bot.configure(
        name=request.name,
        description=request.description,
        personality=request.personality,
        participants=request.participants
    )
    return {"status": "activated"}


@app.post("/participants")
async def update_participants(request: UpdateParticipantsRequest):
    bot.update_participants(request.participants)
    return {"status": "participants updated"}


@app.post("/deactivate")
async def deactivate_bot():
    bot.active = False
    return {"status": "deactivated"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        user_message = await websocket.receive_text()

        bot.add_message("user", user_message)

        if bot.get_total_characters() > 10000:
            old_text = ""
            half = len(bot.memory_messages) // 2

            for msg in bot.memory_messages[:half]:
                old_text += msg["content"] + "\n"

            summary = summarize_text(old_text)
            bot.memory_summary += "\n" + summary

            bot.memory_messages = bot.memory_messages[half:]

        context = bot.build_context()
        response = ask_llm(context)

        bot.add_message("assistant", response)
        await websocket.send_text(response)