from socketio import AsyncClient
import asyncio
from aioconsole import ainput

IpAddress = '127.0.0.1'
PORT = '8080'
ClientName = input('Name you want to show in chat: ')
roomName = input('Enter room (boy/girl): ').strip()

sio = AsyncClient()
FullIp = f'http://{IpAddress}:{PORT}'

@sio.event
async def connect():
    print('Connected to server')
    await sio.emit('join_chat', {'room': roomName, 'name': ClientName})

@sio.event
async def get_message(message):
    if ClientName == message['from']:
        print('You: ' + message['message'])
    else:
        print(message['from'] + ': ' + message['message'])

async def send_message():
    global roomName
    while True:
        await asyncio.sleep(0.01)
        messageTosend = await ainput(': ')

        if messageTosend.lower() == '/exit':
            await sio.emit('exit_chat', {'room': roomName, 'name': ClientName})
            print("You have left the room.")
            roomName = input('Enter new room (boy/girl): ').strip()
            await sio.emit('join_chat', {'room': roomName, 'name': ClientName})
            continue

        if messageTosend.lower() == '/leave':
            await sio.emit('leave_server', {'name': ClientName})
            print("You have left the server.")
            break

        await sio.emit('send_chat_room', {
            'message': messageTosend,
            'name': ClientName,
            'room': roomName
        })

async def main():
    await sio.connect(FullIp)
    await asyncio.gather(send_message(), sio.wait())

if __name__ == '__main__':
    asyncio.run(main())
