import flet as ft
from db import login_user

def login_page(page: ft.Page):
    def login(e):
        email = email_field.value
        password = password_field.value
        
        user = login_user(email, password)
        if user:
            page.session.set("user_id", user["user_id"])
            page.session.set("role", user["role"])
            page.go("/dashboard")
        else:
            error_text.value = "Неверный email или пароль"
            page.update()
    
    email_field = ft.TextField(
        label="Email",
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
    error_text = ft.Text(color="red", size=16)
    login_button = ft.ElevatedButton(
        "Войти",
        on_click=login,
        bgcolor="#4682B4",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=page.width * 0.9,
        height=50
    )
    register_button = ft.TextButton(
        "Зарегистрироваться",
        on_click=lambda _: page.go("/register"),
        style=ft.ButtonStyle(color="#4682B4")
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Авторизация", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
            email_field,
            password_field,
            error_text,
            login_button,
            register_button
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        padding=20,
        bgcolor="#F5F5F5",
        border_radius=10,
        margin=10,
        expand=True
    )