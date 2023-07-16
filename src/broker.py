import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel
from config import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS


class RabbitMQClient:
    """Ассинхронный клиент RabbitMQ"""
    def __init__(self):
        self.connection: AbstractConnection = None
        self.channel: AbstractChannel = None

    async def connect(self):
        """Устанавливает подключение c RabbitMQ и создает канал"""
        try:
            self.connection = await aio_pika.connect(
                f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbit'
            )
            self.channel = await self.connection.channel()
        except Exception as e:
            print(f'Ошибка подключения к брокеру {e}')
            raise e

    async def send_message(self, queue: str, message: str):
        """Отправляет сообщение в указанную очередь
        
        Аргументы:
            queue: Название очереди
            message: Сообщение
        """
        try:
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue,
            )
        except Exception as e:
            print(f'Ошибка отправки сообщения в {queue}: {e}')
            raise e

    async def receive_messages(self, queue: str) -> str:
        """Получает сообщения из указанной очереди
        
        Аргументы:
            queue: Название очереди
        
        Возращает:
            str: Сообщение из очереди
        """
        try:
            queue = await self.channel.declare_queue(queue)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        yield (message.body.decode())
        except Exception as e:
            print(f'Ошибка поулчения из очереди {queue}: {e}')
            raise e


    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            print(f'Сессия завершилась с ошибкой: {exc}')
        await self.connection.close()
