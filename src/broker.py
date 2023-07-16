import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel
from config import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS


class RabbitMQClient:
    def __init__(self):
        self.connection: AbstractConnection = None
        self.channel: AbstractChannel = None

    async def connect(self):
        self.connection = await aio_pika.connect(
            f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbit'
        )
        self.channel = await self.connection.channel()

    async def send_message(self, queue: str, message: str):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue,
        )

    async def receive_messages(self, queue: str) -> str:
        queue = await self.channel.declare_queue(queue)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    yield (message.body.decode())

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()
