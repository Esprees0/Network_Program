const { Sequelize, DataTypes } = require('sequelize');

// ใช้ SQLite เก็บข้อมูล
const sequelize = new Sequelize({
    dialect: 'sqlite',
    storage: 'database.sqlite'
});

// ตาราง User
const User = sequelize.define('User', {
    username: { type: DataTypes.STRING, allowNull: false, unique: true },
    password: { type: DataTypes.STRING, allowNull: false }
});

// ตาราง ChatRoom
const ChatRoom = sequelize.define('ChatRoom', {
    name: { type: DataTypes.STRING, allowNull: false, unique: true }
});

module.exports = { sequelize, User, ChatRoom };
