from .config import settings
import asyncio
import websockets
import json


class BotWebSocketClient:

    def __init__(self, bot, bot_id: int, bot_name: str):
        self.bot = bot
        self.backend_url = settings.backend_url
        self.bot_id = bot_id
        self.bot_name = bot_name

    async def connect(self):
        await asyncio.gather(
            self.listen_global(),
            self.listen_private()
        )

    async def listen_global(self):
        uri = f"{self.backend_url}/ws/global?type=bot&botId={self.bot_id}"
        print(f"Запуска прослушивания глобального вебсокета - {uri}, для бота с id={self.bot_id}")
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                print(f"Полученное сообщение в глобальном чате: {message}")

                try:
                    data = json.loads(message)
                except json.JSONDecodeError as e:
                    print("Broken JSON:", repr(message))
                    continue

                sender = data["sender"]

                if sender == self.bot.bot_name:
                    continue

                content = data["content"]

                self.bot.add_message("global", sender, content)
                self.bot.reflect_relationship(sender, content)

                response = self.bot.generate_response("global")

                print(f"Бот {self.bot_id} отвечает: ", response)

                await websocket.send(json.dumps({
                    "chatId": 10,
                    "botId": self.bot_id,
                    "sender": self.bot.bot_name,
                    "content": response
                }))

    async def listen_private(self):
        uri = f"{self.backend_url}/ws/private?type=bot&botId={self.bot_id}"
        print(f"Запуска прослушивания локального вебсокета - {uri}, для бота с id={self.bot_id}")

        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                print(f"Полученное сообщение в локальном чате: {message}")

                try:
                    data = json.loads(message)
                except json.JSONDecodeError as e:
                    print("Broken JSON:", repr(message))
                    continue

                sender = data["sender"]

                # 🔥 СНАЧАЛА фильтр
                if sender == self.bot.bot_name:
                    continue

                content = data["content"]

                self.bot.add_message("private", sender, content)
                self.bot.reflect_relationship(sender, content)

                response = self.bot.generate_response("private")

                print(f"Бот {self.bot_id} отвечает: ", response)

                await websocket.send(json.dumps({
                    "chatId": self.bot_id,
                    "botId": self.bot_id,
                    "sender": self.bot.bot_name,
                    "content": response
                }))
