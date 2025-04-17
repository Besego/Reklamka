import flet as ft
from database.db import get_db_connection

def contracts_page(page: ft.Page):
    user_id = page.session.get("user_id")
    
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT ContractId, ContractDate, ExpiryDate, Terms FROM Contracts WHERE UserId=?", (user_id,))
        contracts = c.fetchall()
    except Exception as ex:
        conn.close()
        return ft.Column([
            ft.Text("Ваши контракты", size=24),
            ft.Text(f"Ошибка при загрузке контрактов: {str(ex)}", color="red")
        ])
    conn.close()
    
    contract_texts = [ft.Text(f"Контракт {c[0]}: Дата: {c[1]} - Срок действия: {c[2]} - Условия: {c[3]}") for c in contracts]
    back_button = ft.ElevatedButton("Назад", on_click=lambda e: page.go("/dashboard"))
    
    return ft.Column([
        ft.Text("Ваши контракты", size=24),
        *contract_texts,
        back_button,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)