import asyncio
from aiohttp import web
import socketio
from json import dumps
from datetime import datetime

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

clients = {}

@sio.event
async def join_chat(sid, message):
    name = message.get('name', sid)
    room = message['room']
    join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    clients[sid] = {
        'name': name,
        'room': room,
        'join_time': join_time,
        'leave_time': None
    }

    print(f"{name} joined to {room} at {join_time}")
    await sio.enter_room(sid, room)
    await sio.emit('user_joined', {
        'name': name,
        'room': room,
        'join_time': join_time
    }, room=room)
    await sio.emit('get_message', {
        'message': f'{name} joined at {join_time}',
        'from': 'System'
    }, room=room)

@sio.event
async def exit_chat(sid, message):
    room = message['room']
    name = message.get('name', sid)
    leave_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if sid in clients:
        clients[sid]['leave_time'] = leave_time

    print(f"{name} exited from {room} at {leave_time}")

    await sio.emit('user_left', {
        'name': name,
        'room': room,
        'leave_time': leave_time
    }, room=room)

    await sio.leave_room(sid, room)

@sio.event
async def user_joined(data):
    print(f"{data['name']} joined {data['room']} at {data['join_time']}")

@sio.event
async def user_left(data):
    print(f"{data['name']} left {data['room']} at {data['leave_time']}")

@sio.event
async def send_chat_room(sid, message):
    await sio.emit('get_message', {
        'message': message['message'],
        'from': message['name']
    }, room=message['room'])

@sio.event
async def connect(sid, environ):
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

@sio.event
async def disconnect(sid):
    if sid in clients:
        name = clients[sid]['name']
        room = clients[sid]['room']
        leave_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        clients[sid]['leave_time'] = leave_time

        print(f"{name} disconnected from {room} at {leave_time}")
        await sio.emit('user_left', {
            'name': name,
            'room': room,
            'leave_time': leave_time
        }, room=room)


if __name__ == '__main__':
    web.run_app(app)
