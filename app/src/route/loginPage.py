import flet as ft
import bcrypt
from database.db import get_db_connection

def login_page(page: ft.Page):
    def login(e):
        email = email_field.value
        password = password_field.value
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT UserId, PasswordHash, RoleId FROM Users WHERE Email = ?", (email,))
        user = c.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            page.session.set("user_id", user[0])
            page.session.set("role", "admin" if user[2] == 1 else "user")
            page.go("/dashboard" if user[2] == 2 else "/dashboard")
        else:
            error_text.value = "Неверный email или пароль"
            page.update()
    
    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Пароль", password=True)
    error_text = ft.Text(color="red")
    login_button = ft.ElevatedButton("Войти", on_click=login)
    register_button = ft.TextButton("Зарегистрироваться", on_click=lambda _: page.go("/register"))
    
    
    return ft.Column([
        ft.Text("Авторизация", size=24),
        email_field,
        password_field,
        error_text,
        login_button,
        register_button
    ])
    