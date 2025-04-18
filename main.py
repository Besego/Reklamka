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

    page.window.width = 800 
    page.window.height = 700
    page.window.resizable = False  

    init_db()

    def route_change(route):
        page.views.clear()

        if page.route == "/register":
            page.views.append(ft.View(route="/register", controls=[register_page(page)]))
        elif page.route == "/login":
            page.views.append(ft.View(route="/login", controls=[login_page(page)]))
        elif page.route == "/dashboard":
            page.views.append(ft.View(route="/dashboard", controls=[dashboard_page(page)]))
        elif page.route == "/questionnaire" and page.session.get("user_id"):
            page.views.append(ft.View(route="/questionnaire", controls=[questionnaire_page(page)]))
        elif page.route == "/contracts" and page.session.get("user_id"):
            page.views.append(ft.View(route="/contracts", controls=[contracts_page(page)]))    
        elif page.route == "/orders" and page.session.get("user_id"):
            page.views.append(ft.View(route="/orders", controls=[orders_page(page)]))
        elif page.route == "/admin" and page.session.get("role") == "admin":
            page.views.append(ft.View(route="/admin", controls=[admin_page(page)]))
        else:
            page.views.append(ft.View(route="/login", controls=[login_page(page)]))
        
        page.update()

    page.on_route_change = route_change
    page.go("/dashboard")

ft.app(target=main)