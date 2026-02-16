from typing import List, Dict

MAX_MESSAGES = 500
MAX_CHARACTERS = 10000


class BotInstance:
    def __init__(self):
        self.bot_name: str = ""
        self.bot_description: str = ""
        self.bot_personality: str = ""
        self.participants: List[str] = []
        self.relationships: Dict[str, str] = {}

        self.memory_messages: List[Dict] = []
        self.memory_summary: str = ""

        self.active: bool = False

    def configure(self, name: str, description: str, personality: str, participants: List[str]):
        self.bot_name = name
        self.bot_description = description
        self.bot_personality = personality
        self.participants = participants
        self.active = True

    def update_participants(self, participants: List[str]):
        self.participants = participants

    def add_message(self, role: str, content: str):
        self.memory_messages.append({
            "role": role,
            "content": content
        })

        if len(self.memory_messages) > MAX_MESSAGES:
            self.memory_messages = self.memory_messages[-MAX_MESSAGES:]

    def get_total_characters(self):
        text = self.memory_summary
        for msg in self.memory_messages:
            text += msg["content"]
        return len(text)

    def build_context(self):
        context = f"""
Имя: {self.bot_name}
Описание: {self.bot_description}
Личность: {self.bot_personality}
Участники чата: {", ".join(self.participants)}

Отношения: {self.relationships}

Сводка прошлых сообщений:
{self.memory_summary}

Последние сообщения:
"""

        for msg in self.memory_messages:
            context += f"{msg['role']}: {msg['content']}\n"

        return context