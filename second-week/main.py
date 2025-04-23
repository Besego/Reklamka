import flet as ft
from db import init_db
from pages.adminPage import admin_page
from pages.loginPage import login_page
from pages.dashboardPage import dashboard_page
from pages.ordersPage import orders_page
from pages.questionnairePage import questionnaire_page
from pages.contractsPage import contracts_page
from pages.registerPage import register_page

def main(page: ft.Page):
    page.title = "Рекламка"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.resizable = True

    print("Инициализация базы данных...")
    try:
        init_db()
        print("База данных успешно инициализирована")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {str(e)}")

    def route_change(route):
        print(f"Маршрут изменён на: {page.route}")
        print(f"User ID: {page.session.get('user_id')}, Role: {page.session.get('role')}")

        page.views.clear()

        try:
            if page.route == "/register":
                print("Загружаем страницу регистрации...")
                page.views.append(ft.View(route="/register", controls=[register_page(page)]))
            elif page.route == "/login":
                print("Загружаем страницу входа...")
                page.views.append(ft.View(route="/login", controls=[login_page(page)]))
            elif page.route == "/dashboard":
                print("Загружаем страницу дашборда...")
                page.views.append(ft.View(route="/dashboard", controls=[dashboard_page(page)]))
            elif page.route == "/questionnaire" and page.session.get("user_id"):
                print("Загружаем страницу анкеты...")
                page.views.append(ft.View(route="/questionnaire", controls=[questionnaire_page(page)]))
            elif page.route == "/contracts" and page.session.get("user_id"):
                print("Загружаем страницу контрактов...")
                page.views.append(ft.View(route="/contracts", controls=[contracts_page(page)]))    
            elif page.route == "/orders" and page.session.get("user_id"):
                print("Загружаем страницу заказов...")
                page.views.append(ft.View(route="/orders", controls=[orders_page(page)]))
            elif page.route == "/admin" and page.session.get("role") == "admin":
                print("Загружаем страницу администратора...")
                page.views.append(ft.View(route="/admin", controls=[admin_page(page)]))
            else:
                print("Перенаправление на /login из-за неподходящего маршрута или отсутствия user_id/role")
                page.views.append(ft.View(route="/login", controls=[login_page(page)]))
        except Exception as e:
            print(f"Ошибка при загрузке маршрута {page.route}: {str(e)}")
        
        print("Обновляем страницу...")
        page.update()
        print("Страница обновлена")

    page.on_route_change = route_change
    print("Переходим на /dashboard...")
    page.go("/dashboard")

ft.app(target=main)