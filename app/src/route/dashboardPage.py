import flet as ft

def dashboard_page(page: ft.Page):
    role = page.session.get("role")
    
    # Определяем кнопки в зависимости от роли
    buttons = [
        ft.ElevatedButton("Заполнить анкету", on_click=lambda e: page.go("/questionnaire")),
        ft.ElevatedButton("Посмотреть заказы", on_click=lambda e: page.go("/orders")),
        ft.ElevatedButton("Посмотреть контракты", on_click=lambda e: page.go("/contracts")),
        ft.ElevatedButton("Выйти", on_click=lambda e: page.go("/login"))
    ]
    
    if role == "admin":
        buttons.append(ft.ElevatedButton("Панель администратора", on_click=lambda e: page.go("/admin")))
    
    return ft.Column([
        ft.Text("Добро пожаловать!", size=24),
        ft.Text("Выберите действие:"),
        *buttons
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)