import flet as ft
import os
import json
import uuid

class item_c:
    id: str
    name: str
    price: str
    quantity: str

    def to_jsons(self) -> str:
        return f'''
            {{
                "id": "{self.id}",
                "name": "{self.name}",
                "price": "{self.price}",
                "quantity": "{self.quantity}"
            }}
        '''
    def  to_json(self):
        return json.loads(self.to_jsons())
    def __init__(self, name="", price="", quantity="", id=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.id = id or str(uuid.uuid4())
    def __eq__(self, other):
        return self.id == other.id
    def __repr__(self):
        return self.to_jsons()
    def equals_json(self, other):
        return self.id == other.get("id")
    def from_json(json):
        return item_c(id=json.get("id"), name=json.get("name"), price=json.get("price"), quantity=json.get("quantity"))

def items_to_json(items):
    data = {"items": []}
    for item in items:
        data.get("items").append(item.to_json())
    return data
    


def get_url():
    cur_path = os.path.dirname(__file__)
    return "groceries.json"

def write(data):
    with open(get_url(), "w") as f:
        json.dump(data, f, indent=4)

def load():
    if not os.path.exists(get_url()):
        with open(get_url(), "w") as f:
            f.write('{"items": []}')
    with open(get_url(), "r") as f:
        return json.load(f)

@ft.component
def grocery_item(item, items, set_items, delete_item):
    is_editing, set_is_editing = ft.use_state(False)
    name, set_name = ft.use_state("")
    price, set_price = ft.use_state("")
    quantity, set_quantity = ft.use_state("")

    def init():
        set_name(None)
        set_price(None)
        set_quantity(None)
    ft.use_effect(init, [])

    def change_color():
        set_is_editing(True)
    def save_changes(item):
        item_to_save = item_c(id=item.id, name=name or item.name, price=price or item.price, quantity=quantity or item.quantity)
        new_items = [item_to_save if item_to_save == list_item else list_item for list_item in items]
        set_items(new_items)

        write(items_to_json(new_items))
        set_is_editing(False)

    return ft.Row([
        ft.IconButton(
            icon=ft.Icons.EDIT_SHARP, 
            bgcolor=ft.Colors.ERROR_CONTAINER if is_editing else ft.Colors.with_opacity(0, ft.Colors.WHITE),
            on_click=lambda: save_changes(item)
        ),
        ft.TextField(
            value=name,
            hint_text=item.name,
            expand=True,
            on_change=lambda e: (
                change_color(),
                set_name(e.control.value)
            ),
            autocorrect=True,
        ),
        ft.TextField(
            value=price,
            hint_text=f"${item.price}",
            expand=True,
            on_change=lambda e: (
                change_color(),
                set_price(e.control.value)
            ),
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9.]*$")
        ),
        ft.TextField(
            value=quantity,
            hint_text=f"x{item.quantity}",
            expand=True,
            on_change=lambda e: (
                change_color(),
                set_quantity(e.control.value)
            ),
            input_filter=ft.InputFilter(allow=False, regex_string=r"^[0-9.]*$")
        ),
        ft.IconButton(icon=ft.Icons.DELETE_OUTLINE_SHARP, on_click=delete_item(item), icon_color=ft.Colors.ERROR),
    ])

@ft.component
def grocery_page():
    items, set_items = ft.use_state([])
    new_name, set_new_name = ft.use_state("")
    new_price, set_new_price = ft.use_state("")
    new_quantity, set_new_quantity = ft.use_state("")
    
    ft.use_effect(lambda: set_items([item_c.from_json(x) for x in load().get("items")]), [])


    def add_item(e):
        if new_name and new_price and new_quantity:
            the_new_item = item_c(name=new_name, price=new_price, quantity=new_quantity)
            new_items = items + [the_new_item]
            set_items(new_items)
            set_new_name("")
            set_new_price("")
            set_new_quantity("")
            write(items_to_json(new_items))

    def delete_item(item_to_delete):
        def handler(e):
            new_items = [item for item in items if item != item_to_delete]
            set_items(new_items)
            write(items_to_json(new_items))

        return handler
    
    return ft.Column([
        ft.Row([
            ft.TextField(
                value=new_name,
                hint_text="Name",
                on_change=lambda e: set_new_name(e.control.value),
                on_submit=add_item,
                expand=True,
                autocorrect=True,
                autofocus=True,
            ),
            ft.TextField(
                value=new_price,
                hint_text="price",
                on_change=lambda e: set_new_price(e.control.value),
                on_submit=add_item,
                expand=True,
                input_filter=ft.InputFilter(allow=False, regex_string=r"^[0-9.]*$"),
            ),
            ft.TextField(
                value=new_quantity,
                hint_text="quantity",
                on_change=lambda e: set_new_quantity(e.control.value),
                on_submit=add_item,
                expand=True,
                input_filter=ft.InputFilter(allow=False, regex_string=r"^[0-9.]*$"),
            ),
            ft.Button("Add", on_click=add_item),
        ]),
        ft.Column([
            grocery_item(item, items, set_items, delete_item) for item in items if len(items) > 0
        ])
    ])