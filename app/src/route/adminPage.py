import flet as ft
from database.db import get_db_connection

def admin_page(page: ft.Page):
    def approve_order(order_id):
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("UPDATE Orders SET Status='approved' WHERE OrderId=?", (order_id,))
            c.execute("INSERT INTO Contracts (UserId, ContractDate, ExpiryDate, Terms) SELECT UserId, DATE('now'), DATE('now', '+1 year'), 'Стандартные условия' FROM Orders WHERE OrderId=?", (order_id,))
            conn.commit()
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
        finally:
            conn.close()
        page.update()
    
    def reject_order(order_id):
        conn = get_db_connection()
        c = conn.cursor()
        try:
            # Отключаем проверку внешних ключей
            c.execute("PRAGMA foreign_keys=OFF")
            
            # Получаем UserId удаляемой заявки
            c.execute("SELECT UserId FROM Orders WHERE OrderId=?", (order_id,))
            user_id = c.fetchone()[0]
            
            # Удаляем заявку
            c.execute("DELETE FROM Orders WHERE OrderId=?", (order_id,))
            
            # Обновляем OrderId для всех последующих заявок
            c.execute("UPDATE Orders SET OrderId = OrderId - 1 WHERE OrderId > ?", (order_id,))
            
            # Обновляем UserOrderId для заявок текущего пользователя
            c.execute("SELECT OrderId, UserOrderId FROM Orders WHERE UserId=? AND UserOrderId > (SELECT UserOrderId FROM Orders WHERE OrderId=?) ORDER BY UserOrderId",
                    (user_id, order_id))
            user_orders = c.fetchall()
            for order in user_orders:
                new_user_order_id = order[1] - 1
                c.execute("UPDATE Orders SET UserOrderId=? WHERE OrderId=?", (new_user_order_id, order[0]))
            
            # Включаем проверку внешних ключей обратно
            c.execute("PRAGMA foreign_keys=ON")
            
            conn.commit()
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
        finally:
            conn.close()
        page.update()
    
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT OrderId, UserId, Description, Amount, Status FROM Orders")
        orders = c.fetchall()
    except Exception as ex:
        return ft.Column([
            ft.Text("Панель администратора", size=24),
            ft.Text(f"Ошибка: {str(ex)}", color="red")
        ])
    finally:
        conn.close()
    
    error_text = ft.Text(color="red")
    order_rows = []
    for order in orders:
        row = ft.Row([
            ft.Text(f"Заказ {order[0]} (Пользователь {order[1]}): {order[2]} - Сумма: {order[3]} - Статус: {order[4]}"),
            ft.ElevatedButton("Одобрить", on_click=lambda e, oid=order[0]: approve_order(oid), disabled=order[4] != "На рассмотрении"),
            ft.ElevatedButton("Отклонить", on_click=lambda e, oid=order[0]: reject_order(oid), disabled=order[4] != "На рассмотрении")
        ])
        order_rows.append(row)
    
    back_button = ft.ElevatedButton("Назад", on_click=lambda e: page.go("/dashboard"))
    
    return ft.Column([
        ft.Text("Панель администратора", size=24),
        error_text,
        *order_rows,
        back_button
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)