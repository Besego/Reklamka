import sqlite3
import os
import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'advertising_agency.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db_connection()  
    c = conn.cursor()

    # Создание таблиц
    c.execute('''CREATE TABLE IF NOT EXISTS Roles (
        RoleId INTEGER PRIMARY KEY,
        RoleName TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Users (
        UserId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        PasswordHash TEXT NOT NULL,
        Phone TEXT,
        Email TEXT UNIQUE NOT NULL,
        Address TEXT,
        RoleId INTEGER,
        FOREIGN KEY (RoleId) REFERENCES Roles(RoleId)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Materials (
        MaterialId INTEGER PRIMARY KEY AUTOINCREMENT,
        Type TEXT NOT NULL,
        CreatedDate DATE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Orders (
        OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
        UserId INTEGER,
        UserOrderId INTEGER,
        OrderDate DATE,
        Description TEXT,
        Amount REAL,
        Status TEXT,
        MaterialId INTEGER,
        FOREIGN KEY (UserId) REFERENCES Users(UserId),
        FOREIGN KEY (MaterialId) REFERENCES Materials(MaterialId)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Contracts (
        ContractId INTEGER PRIMARY KEY AUTOINCREMENT,
        UserId INTEGER,
        ContractDate DATE,
        ExpiryDate DATE,
        Terms TEXT,
        FOREIGN KEY (UserId) REFERENCES Users(UserId)
    )''')

    # Добавление базовых ролей
    c.execute("INSERT OR IGNORE INTO Roles (RoleId, RoleName) VALUES (1, 'admin')")
    c.execute("INSERT OR IGNORE INTO Roles (RoleId, RoleName) VALUES (2, 'user')")

    # Добавление администратора
    password_hash = bcrypt.hashpw("555555".encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT OR IGNORE INTO Users (Name, PasswordHash, Phone, Email, Address, RoleId) VALUES (?, ?, ?, ?, ?, ?)",
            ("BesegoAdmin", password_hash.decode('utf-8'), "777777", "BesegoAdminka@reklamka.com", "Monaco", 1))

    # # Добавление данных в таблицу Materials
    # materials = [
    #     ("Реклама в автобусах", "2025-04-17"),
    #     ("Флаеры", "2025-04-17"),
    #     ("Плакаты на стенах", "2025-04-17"),
    #     ("Баннеры в интернете", "2025-04-17"),
    #     ("Реклама на радио", "2025-04-17"),
    # ]
    # for material_type, created_date in materials:
    #     c.execute("INSERT OR IGNORE INTO Materials (Type, CreatedDate) VALUES (?, ?)", (material_type, created_date))

    conn.commit()
    conn.close()
