import flet as ft
from datetime import datetime as dt
import people
import tasks
import groceries
import kalendar
import asyncio

# ft.IconButton(ft.Icons.ADD_COMMENT_SHARP),
# ft.IconButton(ft.Icons.ADD_REACTION_SHARP),


#def not written by ai
@ft.component
def clock():
    time_str, set_time_str = ft.use_state(dt.now().strftime("%H:%M:%S"))

    async def tick():
        while True:
            await asyncio.sleep(1)
            today = dt.now()
            set_time_str(f"Kal-E  -  {num_to_month(today.month)} {today.day} {today.year} : {today.strftime('%I:%M:%S %p')}")

    ft.use_effect(lambda: ft.context.page.run_task(tick), [])
    return ft.Text(time_str, size=32, weight=ft.FontWeight.BOLD)

def num_to_month(month_num: int) -> str:
    months = [
        #def didn't have ai write out all the months for me
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
    return months[month_num - 1]

@ft.component
def AppLayout():
    outlet = ft.use_route_outlet()
    navigation_action_padding = ft.Padding.symmetric(vertical=0, horizontal=20)
    today = dt.now()

    page = ft.context.pageMerchant API 
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.theme_mode = ft.ThemeMode.DARK
    page.window.full_screen = True

    return ft.Column(
        [
            ft.Container(
                ft.AppBar(
                    leading=ft.IconButton(ft.Icons.SORT_SHARP, on_click=lambda: ft.context.page.navigate("/")),
                    title=clock(),
                    center_title=True,
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    shape=ft.RoundedRectangleBorder(radius=5),
                    actions=[
                        ft.IconButton(ft.Icons.CALENDAR_MONTH_SHARP,    padding=navigation_action_padding, on_click=lambda: ft.context.page.navigate("/calendar")),
                        ft.IconButton(ft.Icons.SHOPPING_BAG_SHARP,      padding=navigation_action_padding, on_click=lambda: ft.context.page.navigate("/groceries")),
                        ft.IconButton(ft.Icons.WORKSPACE_PREMIUM_SHARP, padding=navigation_action_padding, on_click=lambda: ft.context.page.navigate("/tasks")),
                        ft.IconButton(ft.Icons.PERSON_SHARP,            padding=navigation_action_padding, on_click=lambda: ft.context.page.navigate("/people")),
                        ft.IconButton(ft.Icons.RESTART_ALT_SHARP,       padding=navigation_action_padding, on_click=lambda: ft.context.page.navigate("/groceries")),
                    ],
                ),
                padding=10,
            ),
            ft.Container(content=outlet, padding=20),
        ],
        scroll=ft.ScrollMode.ALWAYS,
    )

@ft.component
def App():
    print("Running\n\n")
    return ft.SafeArea(
        content=ft.Router(
            [
                ft.Route(
                    component=AppLayout,
                    children=[
                        ft.Route(index=True, component=kalendar.calendar_page),
                        ft.Route(path="calendar", component=kalendar.calendar_page),
                        ft.Route(path="groceries", component=groceries.grocery_page),
                        ft.Route(path="tasks", component=tasks.task_page),
                        ft.Route(path="people", component=people.people_page),
                    ],
                ),
            ]
        )
    )    


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))



