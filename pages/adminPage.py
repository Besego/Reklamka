import flet as ft
from db import fetch_orders_for_admin, approve_order, reject_order

def admin_page(page: ft.Page):
    # Получаем заказы
    orders = fetch_orders_for_admin()
    if orders is None:
        return ft.Container(
            content=ft.Column([
                ft.Text("Панель администратора", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Text("Ошибка при загрузке заказов", color="red", size=16)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#F5F5F5",
            border_radius=10,
            margin=10,
            expand=True
        )

    # Создаём изменяемый список заказов
    orders_list = list(orders)  # Преобразуем в изменяемый список

    # Создаём контейнер для карточек заказов
    order_rows_container = ft.Ref[ft.Column]()
    error_text = ft.Text(color="red", size=16)

    def update_order_rows():
        order_rows_container.current.controls.clear()
        for order in orders_list:
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
                            on_click=lambda e, oid=order[0]: handle_approve_order(oid),
                            disabled=not is_pending,
                            bgcolor="#4682B4" if is_pending else "#808080",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            width=120,
                            height=40
                        ),
                        ft.ElevatedButton(
                            "Отклонить",
                            on_click=lambda e, oid=order[0]: handle_reject_order(oid),
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

    def handle_approve_order(order_id):
        if approve_order(order_id):
            # Обновляем локальный список заказов
            for i, order in enumerate(orders_list):
                if order[0] == order_id:
                    updated_order = list(order)
                    updated_order[5] = "Одобрено"
                    orders_list[i] = tuple(updated_order)
                    break
            update_order_rows()
        else:
            error_text.value = "Ошибка при одобрении заказа"
            page.update()

    def handle_reject_order(order_id):
        if reject_order(order_id):
            # Обновляем локальный список заказов
            for i, order in enumerate(orders_list):
                if order[0] == order_id:
                    updated_order = list(order)
                    updated_order[5] = "Отклонено"
                    orders_list[i] = tuple(updated_order)
                    break
            update_order_rows()
        else:
            error_text.value = "Ошибка при отклонении заказа"
            page.update()

    if not orders_list:
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
    for order in orders_list:
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
                        on_click=lambda e, oid=order[0]: handle_approve_order(oid),
                        disabled=not is_pending,
                        bgcolor="#4682B4" if is_pending else "#808080",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        width=120,
                        height=40
                    ),
                    ft.ElevatedButton(
                        "Отклонить",
                        on_click=lambda e, oid=order[0]: handle_reject_order(oid),
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