import asyncio
from broker import RabbitMQClient


async def string_reverser(msg: str):
    return f'input: {msg}, output: {msg[::-1]}'


async def main():
    async with RabbitMQClient() as client:
        async for message in client.receive_messages('string_reverser'):
            output_str = await string_reverser(message)
            await client.send_message('string_out', output_str)


if __name__ == '__main__':
    asyncio.run(main())
