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
        return ft.Column([
            ft.Text("Ваши контракты", size=24),
            ft.Text(f"Ошибка при загрузке контрактов: {str(ex)}", color="red")
        ])
    conn.close()
    
    contract_texts = [ft.Text(f"Контракт {i+1}. Описание заказа: {c[1]} - Дата: {c[2]} - Срок действия: {c[3]} - Условия: {c[4]}") for i, c in enumerate(contracts)]
    back_button = ft.ElevatedButton("Назад", on_click=lambda e: page.go("/dashboard"))
    
    return ft.Column([
        ft.Text("Ваши контракты", size=24),
        *contract_texts,
        back_button,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)