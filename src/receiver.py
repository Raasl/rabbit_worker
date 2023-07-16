from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from broker import RabbitMQClient

app = FastAPI(title='Listener API')


@app.websocket('/listen_results/')
async def listen(websocket: WebSocket):
    try:
        await websocket.accept()
        async with RabbitMQClient() as client:
            async for message in client.receive_messages('string_out'):
                await websocket.send_text(message)
    except WebSocketDisconnect as e:
        print(f'Websocket [{e.code}]: {e.reason}')
