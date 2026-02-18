from typing import List, Dict
from .relationship import Relationship
from .llm_client import ask_yandex
import json
import re


MAX_MESSAGES = 500


class BotInstance:

    def __init__(self):
        self.bot_name: str = ""
        self.bot_description: str = ""
        self.bot_personality: str = ""
        self.participants: List[str] = []

        self.bot_id: int = 0
        self.active: bool = False

        self.mood: str = "neutral"
        self.relationships: Dict[str, Relationship] = {}

        self.global_summary: str = ""

        self.chat_memories = {
            "private": [],
            "global": []
        }

    def configure(self, name, description, personality,
                  participants, bot_id):

        self.bot_name = name
        self.bot_description = description
        self.bot_personality = personality
        self.participants = participants
        self.bot_id = bot_id
        self.active = True

        for p in participants:
            if p != self.bot_name:
                self.relationships[p] = Relationship()

    def add_message(self, chat_type: str, role: str, content: str):

        self.chat_memories[chat_type].append({
            "role": role,
            "content": content
        })

        if len(self.chat_memories[chat_type]) > MAX_MESSAGES:
            self.chat_memories[chat_type] = \
                self.chat_memories[chat_type][-MAX_MESSAGES:]

    def reflect_relationship(self, sender: str, content: str):

        if sender == self.bot_name:
            return

        if sender not in self.relationships:
            return

        current = self.relationships[sender]

        prompt = f"""
Ты — психологический модуль бота {self.bot_name}.

Текущее отношение к {sender}:
trust: {current.trust}
anger: {current.anger}
respect: {current.respect}
mood: {self.mood}

Сообщение от {sender}:
"{content}"

Верни JSON:
{{
  "trust": 0-1,
  "anger": 0-1,
  "respect": 0-1,
  "mood": "neutral/angry/offended/happy"
}}
"""

        response = ask_yandex(prompt)

        try:
            data = json.loads(response)

            current.trust = max(0, min(1, data.get("trust", current.trust)))
            current.anger = max(0, min(1, data.get("anger", current.anger)))
            current.respect = max(0, min(1, data.get("respect", current.respect)))
            self.mood = data.get("mood", self.mood)

        except:
            pass


    def serialize_relationships(self):
        return {
            name: rel.to_dict()
            for name, rel in self.relationships.items()
        }

    def build_context(self, chat_type: str):

        context = f"""
Имя: {self.bot_name}
Описание: {self.bot_description}
Личность: {self.bot_personality}

Настроение: {self.mood}
Отношения: {self.serialize_relationships()}

Участники: {", ".join(self.participants)}

Правило: отвечай не более 250 символов (включая пробелы), 1–2 предложения. 
Если нужно — задай 1 уточняющий вопрос.

Диалог:
"""

        for msg in self.chat_memories[chat_type]:
            context += f"{msg['role']}: {msg['content']}\n"

        return context

    # ------------------------
    # RESPONSE GENERATION
    # ------------------------

    def generate_response(self, chat_type: str):

        context = self.build_context(chat_type)

        response = ask_yandex(context)

        response = self.sanitize_text(response)

        self.add_message(chat_type, "assistant", response)

        return response

    def sanitize_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.replace("\r", "")

        text = text.replace("\n", " ")

        text = re.sub(r'[\x00-\x1f\x7f]', '', text)

        text = re.sub(r'\s+', ' ', text)

        return text.strip()


    def get_info(self):
        return "Имя + ", self.bot_name, ", Айди: ", self.bot_id