import asyncio
from aiohttp import web
import socketio
from datetime import datetime

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

clients = {}
rooms_available = ['boy', 'girl']

@sio.event
async def join_chat(sid, message):
    name = message.get('name', sid)
    room = message['room']

    if room not in rooms_available:
        await sio.emit('get_message', {
            'message': f'Room "{room}" does not exist. Please choose boy or girl.',
            'from': 'System'
        }, room=sid)
        return

    join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    clients[sid] = {
        'name': name,
        'room': room,
        'join_time': join_time,
        'leave_time': None
    }

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

    await sio.emit('user_left', {
        'name': name,
        'room': room,
        'leave_time': leave_time
    }, room=room)
    await sio.leave_room(sid, room)

@sio.event
async def leave_server(sid, message):
    room = clients.get(sid, {}).get('room')
    name = message.get('name', sid)
    leave_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if room:
        await sio.emit('user_left', {
            'name': name,
            'room': room,
            'leave_time': leave_time
        }, room=room)

    if sid in clients:
        del clients[sid]

    await sio.disconnect(sid)

@sio.event
async def send_chat_room(sid, message):
    await sio.emit('get_message', {
        'message': message['message'],
        'from': message['name']
    }, room=message['room'])

@sio.event
async def connect(sid, environ):
    await sio.emit('my_response', {'data': 'Connected'}, room=sid)

@sio.event
async def disconnect(sid):
    if sid in clients:
        del clients[sid]

if __name__ == '__main__':
    web.run_app(app)
