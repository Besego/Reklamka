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
            # Считаем количество заявок пользователя, чтобы определить новый UserOrderId
            c.execute("SELECT COUNT(*) FROM Orders WHERE UserId=?", (user_id,))
            user_order_count = c.fetchone()[0]
            new_user_order_id = user_order_count + 1

            # Добавляем новую заявку с UserOrderId
            c.execute("INSERT INTO Orders (UserId, UserOrderId, OrderDate, Description, Amount, Status, MaterialId) VALUES (?, ?, DATE('now'), ?, ?, 'pending', ?)",
                    (user_id, new_user_order_id, description, amount, material_id))
            conn.commit()
            page.go("/orders")
            page.update()
        except Exception as ex:
            error_text.value = f"Ошибка: {str(ex)}"
            page.update()
        finally:
            conn.close()
    
    # Загружаем материалы из базы данных
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
        value=None
    )

    description_field = ft.TextField(label="Описание")
    amount_field = ft.TextField(label="Сумма")
    error_text = ft.Text(color="red")
    submit_button = ft.ElevatedButton("Отправить", on_click=submit)
    back_button = ft.ElevatedButton("Назад", on_click=lambda e: page.go("/dashboard"))
    
    return ft.Column([
        ft.Text("Анкета", size=24),
        description_field,
        amount_field,
        material_dropdown,
        error_text,
        submit_button,
        back_button
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)