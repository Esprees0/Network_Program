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
    msg_time = message.get('time', datetime.now().strftime('%H:%M:%S'))
    print(f"[{msg_time}] {message['from']}: {message['message']}")

async def send_message():
    global roomName
    while True:
        await asyncio.sleep(0.01)
        messageTosend = await ainput(': ')

        # ออกจากห้องแล้วเลือกใหม่
        if messageTosend.lower() == '/exit':
            # แจ้ง server ให้ทุกคนรู้ทันที
            await sio.emit('exit_chat', {'room': roomName, 'name': ClientName})

            # ค่อยถามว่าจะเข้าห้องไหนใหม่
            roomName = input('Enter new room (boy/girl): ').strip()
            await sio.emit('join_chat', {'room': roomName, 'name': ClientName})
            continue

        # ออกจาก server
        if messageTosend.lower() == '/leave':
            await sio.emit('leave_server', {'name': ClientName})
            break

        # ส่งข้อความ
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
