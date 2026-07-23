import flet as ft
import profile as pro

@ft.component
def people_page():
    if pro.current_user == pro.public_user:
        return ft.Button("log in", on_click=lambda: print("pressed"))
    return ft.Text("People Page")
