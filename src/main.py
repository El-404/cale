import flet as ft
from datetime import datetime as dt

# ft.IconButton(ft.Icons.ADD_COMMENT_SHARP),
# ft.IconButton(ft.Icons.ADD_REACTION_SHARP),

def num_to_month(month_num: int) -> str:
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return months[month_num - 1]lambda: ft.context.page.navigate("/")

def grocery_page(page: ft.Page):
    page.add(ft.Text("Grocery Page"))


def calendar_page(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.theme_mode = ft.ThemeMode.DARK
    page.window.full_screen = True

    today = dt.now()

    def nothing():
        lambda: ft.context.page.navigate("/grocery_page")
        print("Nothing")

    navigation_action_padding = ft.Padding.symmetric(vertical=0, horizontal=20)
    navigation = ft.AppBar(
        leading=ft.IconButton(ft.Icons.SORT_SHARP, on_click=nothing),
        title=ft.Text(f"Kal-e  -  {num_to_month(today.month)} {today.day} {today.year} : {today.strftime('%I:%M %p')}"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        shape=ft.RoundedRectangleBorder(radius=5),
        actions=[
            ft.IconButton(ft.Icons.CALENDAR_MONTH_SHARP,    padding=navigation_action_padding, on_click=nothing),
            ft.IconButton(ft.Icons.SHOPPING_BAG_SHARP,      padding=navigation_action_padding, on_click=nothing),
            ft.IconButton(ft.Icons.WORKSPACE_PREMIUM_SHARP, padding=navigation_action_padding, on_click=nothing),
            ft.IconButton(ft.Icons.RESTART_ALT_SHARP,       padding=navigation_action_padding, on_click=nothing)
        ],
    )


    calendar = ft.GridView(expand=True, max_extent=page.width/7, child_aspect_ratio=1.5, scroll="never", semantic_child_count=7)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i in range(0, 7):
        calendar.controls.append(   
            ft.Container(
                ft.Text(f"{days[i]}"),
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                border=ft.Border.all(3, ft.Colors.SHADOW),
                border_radius=ft.BorderRadius.all(5),
            )
        )
    for i in range(1, 31):
        calendar.controls.append(   
            ft.Container(
                ft.Text(f"Item {i}"),
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                border=ft.Border.all(3, ft.Colors.SHADOW),
                border_radius=ft.BorderRadius.all(5),
            )
        )

    page.add(navigation)
    page.add(calendar)



if __name__ == "__main__":
    ft.run(calendar_page)
