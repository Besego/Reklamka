import flet as ft
from database.db import get_db_connection

def orders_page(page: ft.Page):
    user_id = page.session.get("user_id")
    role = page.session.get("role")
    
    conn = get_db_connection()
    c = conn.cursor()
    try:
        if role == "admin":
            c.execute("SELECT OrderId, UserOrderId, Description, Amount, Status FROM Orders")
        else:
            c.execute("SELECT OrderId, UserOrderId, Description, Amount, Status FROM Orders WHERE UserId=?", (user_id,))
        orders = c.fetchall()
    except Exception as ex:
        conn.close()
        return ft.Column([
            ft.Text("Ваши заказы", size=24),
            ft.Text(f"Ошибка при загрузке заказов: {str(ex)}", color="red")
        ])
    conn.close()
    
    # Используем UserOrderId для отображения
    order_texts = [ft.Text(f"Заказ {o[1]}: {o[2]} - Сумма: {o[3]} - Статус: {o[4]}") for o in orders]
    back_button = ft.ElevatedButton("Назад", on_click=lambda e: page.go("/dashboard"))
    
    return ft.Column([
        ft.Text("Ваши заказы", size=24),
        *order_texts,
        back_button
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)