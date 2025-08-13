const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const bodyParser = require('body-parser');
const { sequelize, User, ChatRoom } = require('./data_base');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(bodyParser.json());
app.use(express.static('public'));

// User
app.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;
        const user = await User.create({ username, password });
        res.json({ success: true, user });
    } catch (err) {
        res.json({ success: false, error: err.message });
    }
});

// สร้างห้องแชท
app.post('/create-room', async (req, res) => {
    try {
        const { name } = req.body;
        const room = await ChatRoom.create({ name });
        res.json({ success: true, room });
    } catch (err) {
        res.json({ success: false, error: err.message });
    }
});

app.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        const user = await User.findOne({ where: { username, password } });
        if (!user) {
            return res.json({ success: false, error: 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง' });
        }
        res.json({ success: true, user });
    } catch (err) {
        res.json({ success: false, error: err.message });
    }
});

app.get('/rooms', async (req_, res) => {
    const rooms = await ChatRoom.findAll();
    res.json(rooms);
});

io.on('connection', (socket) => {
    console.log('New client connected');

    socket.on('joinRoom', (room) => {
        socket.join(room);
        socket.room = room;

        const time = new Date();
        const t = `${time.getHours()}:${time.getMinutes()}:${time.getSeconds()}`;

        // ส่งข้อความ system ว่าเข้าห้อง
        io.to(room).emit('message', { type: 'system', msg: 'มีคนเข้าห้อง', time: t });

        console.log(`User joined room: ${room}`);
    });

    socket.on('message', (msg) => {
        const time = new Date();
        const t = `${time.getHours()}:${time.getMinutes()}:${time.getSeconds()}`;
        io.to(socket.room).emit('message', { type: 'user', msg, user: 'ผู้ใช้', time: t });
    });

    socket.on('disconnect', () => {
        if (socket.room) {
            const time = new Date();
            const t = `${time.getHours()}:${time.getMinutes()}:${time.getSeconds()}`;
            io.to(socket.room).emit('message', { type: 'system', msg: 'มีคนออกห้อง', time: t });
        }
        console.log('Client disconnected');
    });
});


// เริ่มต้นฐานข้อมูลแล้วรันเซิร์ฟเวอร์
sequelize.sync().then(() => {
    server.listen(3000, () => {
        console.log('Server running on http://localhost:3000');
    });
});
