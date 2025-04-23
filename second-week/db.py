import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from dotenv import load_dotenv
import bcrypt
import datetime

load_dotenv()

db_path = os.path.join(os.getenv("ANDROID_APP_DIR", ""), "mydatabase.db")
DATABASE_URL = f"sqlite:///{db_path}"

# Создаём синхронный движок SQLAlchemy для SQLite
engine = create_engine(DATABASE_URL, echo=False)

def get_db_connection():
    """
    Возвращает соединение с базой данных через SQLAlchemy.
    Соединение должно быть закрыто вручную после использования.
    """
    return engine.connect()

def init_db():
    """
    Инициализирует базу данных SQLite, создавая таблицы и добавляя начальные данные.
    """
    conn = get_db_connection()
    try:
        # Создание таблиц
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS Roles (
                RoleId INTEGER PRIMARY KEY,
                RoleName TEXT NOT NULL
            )
        '''))

        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS Users (
                UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                PasswordHash TEXT NOT NULL,
                Phone TEXT,
                Email TEXT UNIQUE NOT NULL,
                Address TEXT,
                RoleId INTEGER,
                FOREIGN KEY (RoleId) REFERENCES Roles(RoleId) ON DELETE SET NULL
            )
        '''))

        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS Materials (
                MaterialId INTEGER PRIMARY KEY AUTOINCREMENT,
                Type TEXT NOT NULL,
                CreatedDate TEXT  -- SQLite использует TEXT для дат
            )
        '''))

        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS Orders (
                OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId INTEGER,
                UserOrderId INTEGER,
                OrderDate TEXT,
                Description TEXT,
                Amount REAL,
                Status TEXT,
                MaterialId INTEGER,
                FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE,
                FOREIGN KEY (MaterialId) REFERENCES Materials(MaterialId) ON DELETE SET NULL
            )
        '''))

        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS Contracts (
                ContractId INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId INTEGER,
                ContractName TEXT,
                ContractDate TEXT,
                ExpiryDate TEXT,
                Terms TEXT,
                FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE
            )
        '''))

        # Добавление базовых ролей
        conn.execute(text("INSERT OR IGNORE INTO Roles (RoleId, RoleName) VALUES (:role_id, :role_name)"),
                    {"role_id": 1, "role_name": "admin"})
        conn.execute(text("INSERT OR IGNORE INTO Roles (RoleId, RoleName) VALUES (:role_id, :role_name)"),
                    {"role_id": 2, "role_name": "user"})

        # Добавление начальных материалов
        conn.execute(text("INSERT OR IGNORE INTO Materials (MaterialId, Type, CreatedDate) VALUES (:material_id, :type, date('now'))"),
                    {"material_id": 1, "type": "Реклама в автобусах"})
        conn.execute(text("INSERT OR IGNORE INTO Materials (MaterialId, Type, CreatedDate) VALUES (:material_id, :type, date('now'))"),
                    {"material_id": 2, "type": "Реклама на стенах"})
        conn.execute(text("INSERT OR IGNORE INTO Materials (MaterialId, Type, CreatedDate) VALUES (:material_id, :type, date('now'))"),
                    {"material_id": 3, "type": "Реклама на радио"})
        conn.execute(text("INSERT OR IGNORE INTO Materials (MaterialId, Type, CreatedDate) VALUES (:material_id, :type, date('now'))"),
                    {"material_id": 4, "type": "Флаеры"})

        # Добавление администратора
        password_hash = bcrypt.hashpw("555555".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn.execute(text('''
            INSERT OR IGNORE INTO Users (Name, PasswordHash, Phone, Email, Address, RoleId)
            VALUES (:name, :password_hash, :phone, :email, :address, :role_id)
        '''), {
            "name": "BesegoAdmin",
            "password_hash": password_hash,
            "phone": "777777",
            "email": "BesegoAdminka@reklamka.com",
            "address": "Monaco",
            "role_id": 1
        })

        conn.commit()
    except SQLAlchemyError as ex:
        print(f"Ошибка при инициализации базы данных: {str(ex)}")
        conn.rollback()
    finally:
        conn.close()

def register_user(name, password, phone, email, address):
    """
    Регистрирует нового пользователя.
    Возвращает True, если регистрация успешна, и False, если email уже существует.
    """
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conn = get_db_connection()
    try:
        conn.execute(text('''
            INSERT INTO Users (Name, PasswordHash, Phone, Email, Address, RoleId)
            VALUES (:name, :password_hash, :phone, :email, :address, :role_id)
        '''), {
            "name": name,
            "password_hash": password_hash,
            "phone": phone,
            "email": email,
            "address": address,
            "role_id": 2  # Роль "user"
        })
        conn.commit()
        return True
    except IntegrityError:
        conn.rollback()
        return False
    except SQLAlchemyError as ex:
        conn.rollback()
        print(f"Ошибка при регистрации пользователя: {str(ex)}")
        return False
    finally:
        conn.close()

def login_user(email, password):
    """
    Проверяет данные пользователя и возвращает информацию о пользователе (user_id, role),
    если авторизация успешна, или None, если email/пароль неверные.
    """
    conn = get_db_connection()
    try:
        result = conn.execute(text('''
            SELECT UserId, PasswordHash, RoleId
            FROM Users
            WHERE Email = :email
        '''), {"email": email})
        user = result.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            role = "admin" if user[2] == 1 else "user"
            return {"user_id": user[0], "role": role}
        return None
    except SQLAlchemyError as ex:
        print(f"Ошибка при авторизации пользователя: {str(ex)}")
        return None
    finally:
        conn.close()

def fetch_orders_for_admin():
    """
    Получает все заказы для панели администратора.
    Возвращает список заказов или None в случае ошибки.
    """
    conn = get_db_connection()
    try:
        result = conn.execute(text('''
            SELECT Orders.OrderId, Orders.UserId, Users.Email, Orders.Description, Orders.Amount, Orders.Status
            FROM Orders
            JOIN Users ON Orders.UserId = Users.UserId
        '''))
        orders = result.fetchall()
        for order in orders:
            print(f"Order ID: {order[0]}, Status: {order[5]}")
        return orders
    except SQLAlchemyError as ex:
        print(f"Ошибка при получении заказов: {str(ex)}")
        return None
    finally:
        conn.close()

def fetch_orders_for_user(user_id, role):
    """
    Получает заказы для пользователя или все заказы, если пользователь - админ.
    Возвращает список заказов или None в случае ошибки.
    """
    conn = get_db_connection()
    try:
        if role == "admin":
            result = conn.execute(text('''
                SELECT OrderId, UserOrderId, Description, Amount, Status
                FROM Orders
            '''))
        else:
            result = conn.execute(text('''
                SELECT OrderId, UserOrderId, Description, Amount, Status
                FROM Orders
                WHERE UserId = :user_id
            '''), {"user_id": user_id})
        orders = result.fetchall()
        print("Orders fetched:", orders)
        return orders
    except SQLAlchemyError as ex:
        print(f"Ошибка при получении заказов: {str(ex)}")
        return None
    finally:
        conn.close()

def approve_order(order_id):
    """
    Одобряет заказ и создаёт контракт.
    Возвращает True при успехе, False в случае ошибки.
    """
    conn = get_db_connection()
    try:
        # Получаем описание заказа
        result = conn.execute(text('''
            SELECT Description, UserId
            FROM Orders
            WHERE OrderId = :order_id
        '''), {"order_id": order_id})
        order = result.fetchone()
        if not order:
            return False

        description, user_id = order

        # Обновляем статус заказа
        conn.execute(text('''
            UPDATE Orders
            SET Status = 'Одобрено'
            WHERE OrderId = :order_id
        '''), {"order_id": order_id})

        # Создаём контракт
        conn.execute(text('''
            INSERT INTO Contracts (UserId, ContractName, ContractDate, ExpiryDate, Terms)
            VALUES (:user_id, :contract_name, date('now'), date('now', '+1 year'), 'Стандартные условия')
        '''), {
            "user_id": user_id,
            "contract_name": description
        })

        conn.commit()
        return True
    except SQLAlchemyError as ex:
        print(f"Ошибка при одобрении заказа: {str(ex)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def reject_order(order_id):
    """
    Отклоняет заказ, меняя его статус на "Отклонено".
    Возвращает True при успехе, False в случае ошибки.
    """
    conn = get_db_connection()
    try:
        conn.execute(text('''
            UPDATE Orders
            SET Status = 'Отклонено'
            WHERE OrderId = :order_id
        '''), {"order_id": order_id})
        conn.commit()
        return True
    except SQLAlchemyError as ex:
        print(f"Ошибка при отклонении заказа: {str(ex)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def fetch_contracts_for_user(user_id):
    """
    Получает контракты пользователя.
    Возвращает список контрактов или None в случае ошибки.
    """
    conn = get_db_connection()
    try:
        result = conn.execute(text('''
            SELECT ContractId, ContractName, ContractDate, ExpiryDate, Terms
            FROM Contracts
            WHERE UserId = :user_id
        '''), {"user_id": user_id})
        contracts = result.fetchall()
        return contracts
    except SQLAlchemyError as ex:
        print(f"Ошибка при получении контрактов: {str(ex)}")
        return None
    finally:
        conn.close()

def fetch_materials():
    """
    Получает все материалы.
    Возвращает список материалов или None в случае ошибки.
    """
    conn = get_db_connection()
    try:
        result = conn.execute(text('''
            SELECT MaterialId, Type
            FROM Materials
        '''))
        materials = result.fetchall()
        return materials
    except SQLAlchemyError as ex:
        print(f"Ошибка при получении материалов: {str(ex)}")
        return None
    finally:
        conn.close()

def create_order(user_id, description, amount, material_id):
    """
    Создаёт новый заказ.
    Возвращает True при успехе, False в случае ошибки.
    """
    conn = get_db_connection()
    try:
        # Получаем количество заказов пользователя для определения UserOrderId
        result = conn.execute(text('''
            SELECT COUNT(*)
            FROM Orders
            WHERE UserId = :user_id
        '''), {"user_id": user_id})
        user_order_count = result.fetchone()[0]
        new_user_order_id = user_order_count + 1

        # Создаём заказ
        conn.execute(text('''
            INSERT INTO Orders (UserId, UserOrderId, OrderDate, Description, Amount, Status, MaterialId)
            VALUES (:user_id, :user_order_id, date('now'), :description, :amount, 'На рассмотрении', :material_id)
        '''), {
            "user_id": user_id,
            "user_order_id": new_user_order_id,
            "description": description,
            "amount": amount,
            "material_id": material_id
        })

        conn.commit()
        return True
    except SQLAlchemyError as ex:
        print(f"Ошибка при создании заказа: {str(ex)}")
        conn.rollback()
        return False
    finally:
        conn.close()