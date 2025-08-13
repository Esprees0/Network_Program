from socketio import AsyncClient
import asyncio
from aioconsole import ainput
from datetime import datetime

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
    if message['from'] != ClientName:
        print(message['from'] + ': ' + message['message'])

@sio.event
async def user_left(data):
    if data['name'] != ClientName:
        print(f"{data['name']} left the room at {data['leave_time']}")

async def send_message():
    global roomName
    while True:
        await asyncio.sleep(0.01)
        messageTosend = await ainput(': ')

        if messageTosend.lower() == '/exit':
            leave_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"You left the room at {leave_time}")
            await sio.emit('exit_chat', {'room': roomName, 'name': ClientName})
            roomName = input('Enter new room (boy/girl): ').strip()
            await sio.emit('join_chat', {'room': roomName, 'name': ClientName})
            continue

        if messageTosend.lower() == '/leave':
            leave_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"You left the server at {leave_time}")
            await sio.emit('leave_server', {'name': ClientName})
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
