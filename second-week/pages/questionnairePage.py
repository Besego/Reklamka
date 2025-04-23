import flet as ft
from db import fetch_materials, create_order

def questionnaire_page(page: ft.Page):
    def submit(e):
        description = description_field.value
        try:
            amount = float(amount_field.value)
            material_id = int(material_dropdown.value) if material_dropdown.value else None
        except ValueError:
            error_text.value = "Сумма должна быть числом, а материал должен быть выбран"
            page.update()
            return
        
        if not description:
            error_text.value = "Поле 'Описание' не может быть пустым"
            page.update()
            return
        
        if material_id is None:
            error_text.value = "Пожалуйста, выберите материал"
            page.update()
            return

        if amount <= 0:
            error_text.value = "Сумма должна быть больше нуля"
            page.update()
            return
        
        user_id = page.session.get("user_id")
        if not user_id:
            error_text.value = "Пользователь не авторизован"
            page.update()
            return
        
        if create_order(user_id, description, amount, material_id):
            page.go("/orders")
        else:
            error_text.value = "Ошибка при создании заказа"
            page.update()
    
    materials = fetch_materials()
    if materials is None:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Анкета", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text("Ошибка при загрузке материалов", color="red", size=16)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            padding=20
        )

    material_dropdown = ft.Dropdown(
        label="Материал",
        options=[
            ft.dropdown.Option(key=str(material[0]), text=material[1]) for material in materials
        ],
        value=None,
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=300
    )

    description_field = ft.TextField(
        label="Описание",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=300
    )
    amount_field = ft.TextField(
        label="Сумма",
        border_radius=10,
        border_color="#4682B4",
        focused_border_color="#4682B4",
        width=300
    )
    error_text = ft.Text(color="red", size=16)
    submit_button = ft.ElevatedButton(
        "Отправить",
        on_click=submit,
        bgcolor="#4682B4",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        height=50
    )
    back_button = ft.ElevatedButton(
        "Назад",
        on_click=lambda e: page.go("/dashboard"),
        bgcolor="#FF4040",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        height=50
    )
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Анкета", size=28, weight=ft.FontWeight.BOLD, color="#333333"),
                description_field,
                amount_field,
                material_dropdown,
                error_text,
                submit_button,
                back_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        padding=20
    )