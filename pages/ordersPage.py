import flet as ft
from db import get_db_connection

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
        print("Orders in orders_page:", orders)  # Отладочный вывод
    except Exception as ex:
        conn.close()
        return ft.Container(
            content=ft.Column([
                ft.Text("Ваши заказы", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                ft.Text(f"Ошибка при загрузке заказов: {str(ex)}", color="red", size=16)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor="#F5F5F5",
            border_radius=10,
            margin=10,
            expand=True
        )
    conn.close()
    
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
            content=ft.Column([
                ft.Text(f"Заказ {o[1]}", size=18, weight=ft.FontWeight.BOLD, color="#4682B4"),
                ft.Text(f"Описание: {o[2]}", size=16, color="#333333"),
                ft.Text(f"Сумма: {o[3]}", size=16, color="#333333"),
                ft.Text(f"Статус: {o[4]}", size=16, color=status_color, weight=ft.FontWeight.BOLD),
            ], spacing=5),
            padding=15,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.colors.with_opacity(0.2, "black")),
            margin=ft.margin.only(bottom=10),
            height=130,
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
            ft.Text("Ваши заказы", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
            ft.Container(
                content=ft.Column(order_rows, spacing=10, scroll=ft.ScrollMode.AUTO),
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