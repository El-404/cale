import flet as ft
import os
import json
import uuid

#I think ai wrote most of this...

def get_url():
    cur_path = os.path.dirname(__file__)
    return os.path.relpath("groceries.json", cur_path)

def write(data):
    with open(get_url(), "w") as f:
        json.dump(data, f, indent=4)

def load():
    if not os.path.exists(get_url()):
        with open(get_url(), "w") as f:
            f.write("")
    with open(get_url(), "r") as f:
        return json.load(f)

@ft.component
def grocery_item(item, items, delete_item):
    is_editing, set_is_editing = ft.use_state(False)
    name, set_name = ft.use_state("")
    price, set_price = ft.use_state("")
    quantity, set_quantity = ft.use_state("")
    purchased, set_purchased = ft.use_state(item.get("purchased", False))

    def init():
        set_name(item.get("name", ""))
        set_price(item.get("price", ""))
        set_quantity(item.get("quantity", ""))
        # set_purchased(item.get("purchased", False))
    ft.use_effect(init, [])

    def change_color():
        set_is_editing(True)
    def save_changes(item):
        temp = {"items": []}
        item = {
            "id": item.get("id", ""),
            "name": name,
            "price": price,
            "quantity": quantity,
            "purchased": purchased
        }
        for og_item in enumerate(items.get("items", [])):
            if og_item[1].get("id", "") == item.get("id"):
                temp.get("items", []).append(item)
            else:
                temp.get("items", []).append(og_item[1])
        write(temp)

    return ft.Row([
        ft.IconButton(
            icon=ft.Icons.EDIT_SHARP, 
            bgcolor=ft.Colors.ERROR_CONTAINER if is_editing else ft.Colors.with_opacity(0, ft.Colors.WHITE),
            on_click=lambda: save_changes(item)
        ),
        ft.TextField(
            value=name,
            hint_text=item.get("name", ""),
            expand=True,
            on_change=lambda e: (
                change_color(),
                set_name(e.control.value)
            ),
            autocorrect=True,
        ),
        ft.TextField(
            value=price,
            hint_text=f"${item.get("price", "")}",
            expand=True,
            on_change=lambda e: (
                change_color(),
                set_price(e.control.value)
            ),
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9.]*$")
        ),
        ft.TextField(
            value=quantity,
            hint_text=f"x{item.get("quantity")}",
            expand=True,
            on_change=lambda e: (
                change_color(),
                set_quantity(e.control.value)
            ),
            input_filter=ft.InputFilter(allow=False, regex_string=r"^[0-9]*$")
        ),
        ft.IconButton(icon=ft.Icons.DELETE_OUTLINE_SHARP, on_click=delete_item(item.get("id", "")), icon_color=ft.Colors.ERROR),
    ])

@ft.component
def grocery_page():
    items, set_items = ft.use_state({})
    new_item, set_new_item = ft.use_state("")

    data = load()    
    ft.use_effect(lambda: set_items(data), [])


    def add_item(e):
        if new_item:
            data.get("items", []).append(json.loads(new_item))
            # uuid.uuid4()
            set_items(data)
            set_new_item("")
            write(data)

    def delete_item(id):
        def handler(e):
            temp = {"items": []}
            # print(id)
            for i in enumerate(items.get("items")):
                # print(i[1])
                if i[1].get("id", "") == id:
                    continue
                temp.get("items", []).append(i[1])
            # print(temp)
            set_items(temp)
            write(temp)
        return handler
        


    return ft.Column([
        ft.Row([
            ft.TextField(
                value=new_item,
                hint_text="Add grocery item",
                on_change=lambda e: set_new_item(e.control.value),
                on_submit=add_item,
                expand=True,
                autocorrect=True,
                autofocus=True,
            ),
            ft.Button("Add", on_click=add_item),
        ]),
        ft.Column([
            grocery_item(item, items, delete_item)
            for i, item in enumerate(items.get("items", []))
        ]),
    ])