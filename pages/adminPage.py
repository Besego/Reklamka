import flet as ft
from db import get_db_connection

def admin_page(page: ft.Page):
    # Определяем все функции в начале
    def fetch_orders():
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("""
                SELECT Orders.OrderId, Orders.UserId, Users.Email, Orders.Description, Orders.Amount, Orders.Status
                FROM Orders
                JOIN Users ON Orders.UserId = Users.UserId
            """)
            fetched_orders = c.fetchall()
            for order in fetched_orders:
                print(f"Order ID: {order[0]}, Status: {order[5]}")
            return fetched_orders
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
            return []
        finally:
            conn.close()
    
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
            # Обновляем список заказов
            for i, order in enumerate(orders):
                if order[0] == order_id:
                    updated_order = list(order)
                    updated_order[5] = "Одобрено"
                    orders[i] = tuple(updated_order)
                    break
            update_order_rows()
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
        finally:
            conn.close()
    
    def reject_order(order_id):
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("UPDATE Orders SET Status='Отклонено' WHERE OrderId=?", (order_id,))
            conn.commit()
            # Обновляем список заказов
            for i, order in enumerate(orders):
                if order[0] == order_id:
                    updated_order = list(order)
                    updated_order[5] = "Отклонено"
                    orders[i] = tuple(updated_order)
                    break
            update_order_rows()
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
        finally:
            conn.close()

    # Создаём изменяемый список заказов
    orders = []
    orders.extend(fetch_orders())

    # Создаём контейнер для карточек заказов
    order_rows_container = ft.Ref[ft.Column]()
    error_text = ft.Text(color="red", size=16)

    def update_order_rows():
        order_rows_container.current.controls.clear()
        for order in orders:
            is_pending = order[5].strip().lower() == "на рассмотрении"
            row = ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"Заказ {order[0]} (Пользователь: {order[2]}): {order[3]} - Сумма: {order[4]} - Статус: {order[5]}",
                        size=16,
                        color="#333333",
                        max_lines=5,
                        overflow=ft.TextOverflow.ELLIPSIS,
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
                    ], alignment=ft.MainAxisAlignment.END)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15,
                bgcolor="white",
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.with_opacity(0.2, "black")),
                margin=ft.margin.only(bottom=10),
                width=page.width - 40
            )
            order_rows_container.current.controls.append(row)
        page.update()
    
    if not orders:
        return ft.Container(
            content=ft.Column([
                ft.Text("Панель администратора", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Text("Нет заказов для отображения", color="red", size=16)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#F5F5F5",
            border_radius=10,
            margin=10,
            expand=True
        )
    
    order_rows = []
    for order in orders:
        is_pending = order[5].strip().lower() == "на рассмотрении"
        row = ft.Container(
            content=ft.Column([
                ft.Text(
                    f"Заказ {order[0]} (Пользователь: {order[2]}): {order[3]} - Сумма: {order[4]} - Статус: {order[5]}",
                    size=16,
                    color="#333333",
                    max_lines=5,
                    overflow=ft.TextOverflow.ELLIPSIS,
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
                ], alignment=ft.MainAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.with_opacity(0.2, "black")),
            margin=ft.margin.only(bottom=10),
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
                content=ft.Column(
                    ref=order_rows_container,
                    controls=order_rows,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                ),
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