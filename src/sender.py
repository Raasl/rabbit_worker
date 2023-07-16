from fastapi import FastAPI
from pydantic import BaseModel
from broker import RabbitMQClient

app = FastAPI(title='Sender API')


class Message(BaseModel):
    text: str


@app.post("/queue_reverse_text/")
async def send_to_worker(msg: Message):
    async with RabbitMQClient() as client:
        await client.send_message('string_reverser', msg.text)
