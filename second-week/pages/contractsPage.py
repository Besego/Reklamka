import flet as ft
from db import fetch_contracts_for_user

def contracts_page(page: ft.Page):
    user_id = page.session.get("user_id")
    
    contracts = fetch_contracts_for_user(user_id)
    if contracts is None:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Ваши контракты", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text("Ошибка при загрузке контрактов", color="red", size=16)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            padding=20
        )
    
    contract_rows = []
    for i, c in enumerate(contracts):
        row = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Контракт {i+1}.", size=18, weight=ft.FontWeight.BOLD, color="#4682B4"),
                    ft.Text(f"Описание заказа: {c[1]}", size=16, color="#333333"),
                    ft.Text(f"Дата: {c[2]}", size=16, color="#333333"),
                    ft.Text(f"Срок действия: {c[3]}", size=16, color="#333333"),
                    ft.Text(f"Условия: {c[4]}", size=16, color="#333333"),
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
        contract_rows.append(row)
    
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
                ft.Text("Ваши контракты", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Column(contract_rows, spacing=10, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER),
                back_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        padding=20
    )