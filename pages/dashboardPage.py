import flet as ft

def dashboard_page(page: ft.Page):
    user_id = page.session.get("user_id")
    
    if not user_id:
        def redirect_to_login(e):
            page.go("/login")
        
        buttons = [
            ft.ElevatedButton(
                "Заполнить анкету",
                on_click=redirect_to_login,
                bgcolor="#4682B4",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Посмотреть заказы",
                on_click=redirect_to_login,
                bgcolor="#4682B4",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Посмотреть контракты",
                on_click=redirect_to_login,
                bgcolor="#4682B4",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Авторизация",
                on_click=lambda e: page.go("/login"),
                bgcolor="#32CD32",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Регистрация",
                on_click=lambda e: page.go("/register"),
                bgcolor="#32CD32",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            )
        ]
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Добро пожаловать!", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Text("Необходима авторизация", color="red", size=16),
                ft.Text("Выберите действие:", size=20, color="#333333"),
                ft.Column(buttons, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#F5F5F5",
            border_radius=10,
            margin=10,
            expand=True
        )
    
    role = page.session.get("role")
    
    if role == "admin":
        buttons = [
            ft.ElevatedButton(
                "Панель администратора",
                on_click=lambda e: page.go("/admin"),
                bgcolor="#4682B4",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Выйти",
                on_click=lambda e: page.go("/login"),
                bgcolor="#FF4040",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            )
        ]
    else:
        buttons = [
            ft.ElevatedButton(
                "Заполнить анкету",
                on_click=lambda e: page.go("/questionnaire"),
                bgcolor="#4682B4",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Посмотреть заказы",
                on_click=lambda e: page.go("/orders"),
                bgcolor="#4682B4",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Посмотреть контракты",
                on_click=lambda e: page.go("/contracts"),
                bgcolor="#4682B4",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            ),
            ft.ElevatedButton(
                "Выйти",
                on_click=lambda e: page.go("/login"),
                bgcolor="#FF4040",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=page.width * 0.9,
                height=50
            )
        ]
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Добро пожаловать!", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
            ft.Text("Выберите действие:", size=20, color="#333333"),
            ft.Column(buttons, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor="#F5F5F5",
        border_radius=10,
        margin=10,
        expand=True
    )