from pydantic import BaseModel
from typing import List


class ActivateRequest(BaseModel):
    name: str
    description: str
    personality: str
    participants: List[str]
    bot_id: int


class WSMessage(BaseModel):
    sender: str
    content: str