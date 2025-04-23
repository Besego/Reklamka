import flet as ft
from db import login_user

def login_page(page: ft.Page):
    print("login_page: Начало выполнения")
    def login(e):
        print("login_page: Клик по кнопке Войти")
        email = email_field.value
        password = password_field.value
        
        user = login_user(email, password)
        if user:
            print(f"login_page: Пользователь авторизован, user_id={user['user_id']}, role={user['role']}")
            page.session.set("user_id", user["user_id"])
            page.session.set("role", user["role"])
            page.go("/dashboard")
        else:
            print("login_page: Ошибка авторизации")
            error_text.value = "Неверный email или пароль"
            page.update()
    
    email_field = ft.TextField(
        label="Email",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=300
    )
    password_field = ft.TextField(
        label="Пароль",
        password=True,
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=300
    )
    error_text = ft.Text(color="red", size=16)
    login_button = ft.ElevatedButton(
        "Войти",
        on_click=login,
        bgcolor="#4682B4",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        height=50
    )
    register_button = ft.TextButton(
        "Зарегистрироваться",
        on_click=lambda _: page.go("/register"),
        style=ft.ButtonStyle(color="#4682B4")
    )
    
    print("login_page: Возвращаем Column")
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Авторизация", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                email_field,
                password_field,
                error_text,
                login_button,
                register_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        padding=20
    )