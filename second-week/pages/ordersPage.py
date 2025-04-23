import flet as ft
from db import fetch_orders_for_user

def orders_page(page: ft.Page):
    user_id = page.session.get("user_id")
    role = page.session.get("role")
    
    orders = fetch_orders_for_user(user_id, role)
    if orders is None:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Ваши заказы", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text("Ошибка при загрузке заказов", color="red", size=16)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            padding=20
        )
    
    order_rows = []
    for o in orders:
        status = o[4].strip().lower()
        if status == "на рассмотрении":
            status_color = "#FFA500"
        elif status == "одобрено":
            status_color = "#32CD32"
        elif status == "отклонено":
            status_color = "#FF4040"
        else:
            status_color = "#333333"
        
        row = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Заказ {o[1]}", size=18, weight=ft.FontWeight.BOLD, color="#4682B4"),
                    ft.Text(f"Описание: {o[2]}", size=16, color="#333333"),
                    ft.Text(f"Сумма: {o[3]}", size=16, color="#333333"),
                    ft.Text(f"Статус: {o[4]}", size=16, color=status_color, weight=ft.FontWeight.BOLD),
                ],
                spacing=5
            ),
            padding=15,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.with_opacity(0.2, "black")),
            margin=ft.margin.only(bottom=10),
            width=300
        )
        order_rows.append(row)
    
    back_button = ft.ElevatedButton(
        "Назад",
        on_click=lambda e: page.go("/dashboard"),
        bgcolor="#4682B4",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        height=50
    )
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Ваши заказы", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Column(order_rows, spacing=10, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER),
                back_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        padding=20
    )