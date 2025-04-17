import flet as ft
import sqlite3
import bcrypt
from database.db import get_db_connection

def register_page(page: ft.Page):
    def register(e):
        name = name_field.value
        password = password_field.value
        phone = phone_field.value
        email = email_field.value
        address = address_field.value
        
        # Хэширование пароля
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Сохранение в базу данных
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Users (Name, PasswordHash, Phone, Email, Address, RoleId) VALUES (?, ?, ?, ?, ?, 2)",
                    (name, password_hash.decode('utf-8'), phone, email, address))
            conn.commit()
            page.go("/login")
        except sqlite3.IntegrityError:
            error_text.value = "Этот email уже зарегистрирован"
            page.update()
        finally:
            conn.close()
    
    name_field = ft.TextField(label="Имя")
    password_field = ft.TextField(label="Пароль", password=True)
    phone_field = ft.TextField(label="Телефон")
    email_field = ft.TextField(label="Email")
    address_field = ft.TextField(label="Адрес")
    error_text = ft.Text(color="red")
    register_button = ft.ElevatedButton("Зарегистрироваться", on_click=register)
    login_button = ft.TextButton("Есть аккаунт?", on_click=lambda _: page.go("/login"))
    
    # Возвращаем Column вместо page.add()
    return ft.Column([
        ft.Text("Регистрация", size=24),
        name_field,
        password_field,
        phone_field,
        email_field,
        address_field,
        error_text,
        register_button,
        login_button
    ])