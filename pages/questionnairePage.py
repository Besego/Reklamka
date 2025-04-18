import flet as ft
from db import get_db_connection

def questionnaire_page(page: ft.Page):
    def submit(e):
        description = description_field.value
        try:
            amount = float(amount_field.value)
            material_id = int(material_dropdown.value)
        except ValueError:
            error_text.value = "Сумма должна быть числом, а материал должен быть выбран"
            page.update()
            return
        
        user_id = page.session.get("user_id")
        if not user_id:
            error_text.value = "Пользователь не авторизован"
            page.update()
            return
        
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM Orders WHERE UserId=?", (user_id,))
            user_order_count = c.fetchone()[0]
            new_user_order_id = user_order_count + 1
            c.execute("INSERT INTO Orders (UserId, UserOrderId, OrderDate, Description, Amount, Status, MaterialId) VALUES (?, ?, DATE('now'), ?, ?, 'На рассмотрении', ?)",
                    (user_id, new_user_order_id, description, amount, material_id))
            conn.commit()
            page.go("/orders")
            page.update()
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
        finally:
            conn.close()
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT MaterialId, Type FROM Materials")
    materials = c.fetchall()
    conn.close()

    material_dropdown = ft.Dropdown(
        label="Материал",
        options=[
            ft.dropdown.Option(key=str(material[0]), text=material[1]) for material in materials
        ],
        value=None,
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )

    description_field = ft.TextField(
        label="Описание",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )
    amount_field = ft.TextField(
        label="Сумма",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=page.width * 0.9
    )
    error_text = ft.Text(color="red", size=16)
    submit_button = ft.ElevatedButton(
        "Отправить",
        on_click=submit,
        bgcolor="#4682B4",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=page.width * 0.9,
        height=50
    )
    back_button = ft.ElevatedButton(
        "Назад",
        on_click=lambda e: page.go("/dashboard"),
        bgcolor="#FF4040",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=page.width * 0.9,
        height=50
    )
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Анкета", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
            description_field,
            amount_field,
            material_dropdown,
            error_text,
            submit_button,
            back_button
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        padding=20,
        bgcolor="#F5F5F5",
        border_radius=10,
        margin=10,
        expand=True
    )