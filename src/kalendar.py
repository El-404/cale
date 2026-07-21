import flet as ft
from datetime import datetime as dt
from calendar import monthrange

#def not written by ai
def get_ordinal_suffix(day: int) -> str:
    if 11 <= day <= 13:
        return "th"
    last_digit = day % 10
    if last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    else:
        return "th"

@ft.component
def calendar_page():
    page = ft.context.page
    calendar = ft.GridView(expand=True, max_extent=page.width/7, child_aspect_ratio=1.5)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    today = dt.now()
    first_day, num_days = monthrange(today.year, today.month)

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
    
    for i in range(0, first_day+1):
        content = ft.Container(
            alignment=ft.Alignment.CENTER,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border=ft.Border.all(3, ft.Colors.SHADOW),
            border_radius=ft.BorderRadius.all(5),
        )
        calendar.controls.append(content)

    for i in range(1, num_days+1):
        content = ft.Container(
            ft.Text(f"{i}{get_ordinal_suffix(i)}"),
            alignment=ft.Alignment.CENTER,
            bgcolor=ft.Colors.PRIMARY_CONTAINER if i == today.day else ft.Colors.SURFACE_CONTAINER,
            border=ft.Border.all(3, ft.Colors.SHADOW),
            border_radius=ft.BorderRadius.all(5),
        )
        calendar.controls.append(content)
    if first_day+num_days+1 < 35:
        for i in range(0, 34 - first_day - num_days):
            content = ft.Container(
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                border=ft.Border.all(3, ft.Colors.SHADOW),
                border_radius=ft.BorderRadius.all(5),
            )
            calendar.controls.append(content)

    return calendar