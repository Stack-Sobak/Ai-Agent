import asyncio
import websockets
import json


class BotWebSocketClient:

    def __init__(self, bot, backend_url: str, bot_id: int, bot_name: str):
        self.bot = bot
        self.backend_url = backend_url
        self.bot_id = bot_id
        self.bot_name = bot_name

    async def connect(self):
        await asyncio.gather(
            self.listen_global(),
            self.listen_private()
        )

    async def listen_global(self):
        uri = f"{self.backend_url}/ws/global?type=bot&botId={self.bot_id}"

        print("Connecting to global WebSocket at {uri}", uri)

        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)

                print("Message!!!!")
                sender = data["sender"]
                content = data["content"]

                self.bot.add_message("global", sender, content)
                self.bot.reflect_relationship(sender, content)

                response = self.bot.generate_response("global")

                await websocket.send(json.dumps({
                    "sender": self.bot.bot_name,
                    "content": response
                }))

    async def listen_private(self):
        uri = f"{self.backend_url}/ws/private?type=bot&botId={self.bot_id}"
        print(f"Connecting to private WebSocket at {uri}...")

        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)


                print("Message!!!!")
                sender = data["sender"]
                content = data["content"]

                self.bot.add_message("private", sender, content)
                self.bot.reflect_relationship(sender, content)

                response = self.bot.generate_response("private")

                await websocket.send(json.dumps({
                    "chatId": "1",
                    "sender": self.bot.bot_name,
                    "content": response
                }))