import flet as ft
from db import get_db_connection

def admin_page(page: ft.Page):
    def approve_order(order_id):
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT Description FROM Orders WHERE OrderId=?", (order_id,))
            description = c.fetchone()[0]
            c.execute("UPDATE Orders SET Status='Одобрено' WHERE OrderId=?", (order_id,))
            c.execute("""
                INSERT INTO Contracts (UserId, ContractName, ContractDate, ExpiryDate, Terms)
                SELECT UserId, ?, DATE('now'), DATE('now', '+1 year'), 'Стандартные условия'
                FROM Orders WHERE OrderId=?
            """, (description, order_id))
            conn.commit()
            page.go("/admin")
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
        finally:
            conn.close()
    
    def reject_order(order_id):
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("PRAGMA foreign_keys=OFF")
            c.execute("SELECT UserId FROM Orders WHERE OrderId=?", (order_id,))
            user_id = c.fetchone()[0]
            c.execute("DELETE FROM Orders WHERE OrderId=?", (order_id,))
            c.execute("UPDATE Orders SET OrderId = OrderId - 1 WHERE OrderId > ?", (order_id,))
            c.execute("SELECT OrderId, UserOrderId FROM Orders WHERE UserId=? AND UserOrderId > (SELECT UserOrderId FROM Orders WHERE OrderId=?) ORDER BY UserOrderId",
                    (user_id, order_id))
            user_orders = c.fetchall()
            for order in user_orders:
                new_user_order_id = order[1] - 1
                c.execute("UPDATE Orders SET UserOrderId=? WHERE OrderId=?", (new_user_order_id, order[0]))
            c.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            page.go("/admin")
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
        finally:
            conn.close()
    
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("""
            SELECT Orders.OrderId, Orders.UserId, Users.Email, Orders.Description, Orders.Amount, Orders.Status
            FROM Orders
            JOIN Users ON Orders.UserId = Users.UserId
        """)
        orders = c.fetchall()
        for order in orders:
            print(f"Order ID: {order[0]}, Status: {order[5]}")
    except Exception as ex:
        return ft.Container(
            content=ft.Column([
                ft.Text("Панель администратора", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Text(f"Ошибка: {str(ex)}", color="red", size=16)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#F5F5F5",
            border_radius=10,
            margin=10,
            expand=True
        )
    finally:
        conn.close()
    
    error_text = ft.Text(color="red", size=16)
    order_rows = []
    for order in orders:
        is_pending = order[5].strip().lower() == "на рассмотрении"
        row = ft.Container(
            content=ft.Row([
                ft.Text(
                    f"Заказ {order[0]} (Пользователь: {order[2]}): {order[3]} - Сумма: {order[4]} - Статус: {order[5]}",
                    size=16,
                    color="#333333",
                    expand=True
                ),
                ft.Row([
                    ft.ElevatedButton(
                        "Одобрить",
                        on_click=lambda e, oid=order[0]: approve_order(oid),
                        disabled=not is_pending,
                        bgcolor="#4682B4" if is_pending else "#808080",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        width=120,
                        height=40
                    ),
                    ft.ElevatedButton(
                        "Отклонить",
                        on_click=lambda e, oid=order[0]: reject_order(oid),
                        disabled=not is_pending,
                        bgcolor="#FF4040" if is_pending else "#808080",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        width=120,
                        height=40
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.with_opacity(0.2, "black")),
            margin=ft.margin.only(bottom=10),
            height=90,
            width=page.width - 40
        )
        order_rows.append(row)
    
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
            ft.Text("Панель администратора", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
            error_text,
            ft.Container(
                content=ft.Column(order_rows, spacing=10, scroll=ft.ScrollMode.AUTO),
                height=510,
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