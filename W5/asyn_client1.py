from socketio import AsyncClient
import asyncio
from json import dumps
from aioconsole import ainput

if __name__ == '__main__':
    IpAddress = '127.0.0.1'
    PORT = '8080'
    ClientName = 'Deadpool'
    roomName = 'Marvel'
    messageTosend = ''

    sio = AsyncClient()
    FullIp = 'http://'+IpAddress+':'+PORT

    @sio.event
    async def connect():
        print('Connected to server')
        await sio.emit('join_chat', {'room': roomName,'name': ClientName})

    @sio.event
    async def get_message(message):
        if ClientName == message['from']:
            print('You : ' + message['message'])
        else:
            print(message['from']+' : '+message['message'])

    async def send_message():
        while True:
            await asyncio.sleep(0.01)
            messageTosend = await ainput()
            await sio.emit('send_chat_room', {'message': messageTosend,'name': ClientName, 'room': roomName})
        
    async def connectToserver():
        await sio.connect(FullIp)
        await sio.wait()
    
    async def main(IpAddress):
        await asyncio.gather(
            connectToserver(),
            send_message()
        )

    asyncio.run(main(FullIp))
