import flet as ft
from db import get_db_connection

def contracts_page(page: ft.Page):
    user_id = page.session.get("user_id")
    
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT ContractId, ContractName, ContractDate, ExpiryDate, Terms FROM Contracts WHERE UserId=?", (user_id,))
        contracts = c.fetchall()
    except Exception as ex:
        conn.close()
        return ft.Container(
            content=ft.Column([
                ft.Text("Ваши контракты", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Text(f"Ошибка при загрузке контрактов: {str(ex)}", color="red", size=16)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#F5F5F5",
            border_radius=10,
            margin=10,
            expand=True
        )
    conn.close()
    
    contract_rows = []
    for i, c in enumerate(contracts):
        row = ft.Container(
            content=ft.Column([
                ft.Text(f"Контракт {i+1}.", size=18, weight=ft.FontWeight.BOLD, color="#4682B4"),
                ft.Text(f"Описание заказа: {c[1]}", size=16, color="#333333"),
                ft.Text(f"Дата: {c[2]}", size=16, color="#333333"),
                ft.Text(f"Срок действия: {c[3]}", size=16, color="#333333"),
                ft.Text(f"Условия: {c[4]}", size=16, color="#333333"),
            ], spacing=5),
            padding=15,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.with_opacity(0.2, "black")),
            margin=ft.margin.only(bottom=10),
            height=130,
            width=page.width - 40
        )
        contract_rows.append(row)
    
    back_button = ft.ElevatedButton(
        "Назад",
        on_click=lambda e: page.go("/dashboard"),
        bgcolor="#4682B4",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=150,
        height=50
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Ваши контракты", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
            ft.Container(
                content=ft.Column(contract_rows, spacing=10, scroll=ft.ScrollMode.AUTO),
                height=540,
                expand=True
            ),
            back_button
        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor="#F5F5F5",
        border_radius=10,
        margin=10,
        expand=True
    )