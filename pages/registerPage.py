import flet as ft
import sqlite3
import bcrypt
from db import get_db_connection

def register_page(page: ft.Page):
    def register(e):
        name = name_field.value
        password = password_field.value
        phone = phone_field.value
        email = email_field.value
        address = address_field.value

        if not name or not password or not phone or not email or not address:
            error_text.value = "Все поля обязательны для заполнения"
            page.update()
            return
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
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
    
    name_field = ft.TextField(
        label="Имя",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )
    password_field = ft.TextField(
        label="Пароль",
        password=True,
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )
    phone_field = ft.TextField(
        label="Телефон",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )
    email_field = ft.TextField(
        label="Email",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )
    address_field = ft.TextField(
        label="Адрес",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )
    error_text = ft.Text(color="red", size=16)
    register_button = ft.ElevatedButton(
        "Зарегистрироваться",
        on_click=register,
        bgcolor="#4682B4",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=page.width * 0.9,
        height=50
    )
    login_button = ft.TextButton(
        "Есть аккаунт?",
        on_click=lambda _: page.go("/login"),
        style=ft.ButtonStyle(color="#4682B4")
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Регистрация", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
            name_field,
            password_field,
            phone_field,
            email_field,
            address_field,
            error_text,
            register_button,
            login_button
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        padding=20,
        bgcolor="#F5F5F5",
        border_radius=10,
        margin=10,
        expand=True
    )