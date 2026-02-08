import logging
import orjson
from redis.asyncio import Redis


class RedisPublisher:
    def __init__(self, redis: Redis, channel: str) -> None:
        self._redis = redis
        self._channel = channel
        self._logger = logging.getLogger(__name__)

    async def publish(self, event: dict) -> None:
        message = orjson.dumps(event)

        await self._redis.publish(self._channel, message)

        self._logger.info(
            "event_publisher",
            extra={
                "channel": self._channel,
                "event_type": event.get("event_type"),
                "event_id": event.get("event_id"),
            },
        )
