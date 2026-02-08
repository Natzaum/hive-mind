import discord
import logging
import uuid
from app.redis.publisher import RedisPublisher


class DiscordClient(discord.Client):
    def __init__(self, publisher: RedisPublisher):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents)

        self._publisher = publisher
        self._logger = logging.getLogger(__name__)

    async def on_ready(self):
        self._logger.info("discord_connected", extra={"bot_user": str(self.user)})

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": "message_created",
            "source": "discord",
            "payload": {
                "message_id": message.id,
                "channel_id": message.channel.id,
                "author_id": message.author.id,
                "content": message.content,
            },
        }

        await self._publisher.publish(event)
