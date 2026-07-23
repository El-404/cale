import uuid
import os
import json

class user:
    id: str
    name: str

    def __init__(self, name, id=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
    def __eq__(self, other):
        return self.id == other.id if type(other) == user else self.id == other.get("id", "") if type(other) == dict else self.id == other
    def get_dir(self):
        return self.name + "/"
    def save(self):
        data = {}
        if load(self.id):
            data = {"people": [person if person != self else self.to_json() for person in load().get("people")]}
        else:
            data = load()
            data.get("people").append(self.to_json())
        with open("profiles.json", "w") as f:
            json.dump(data, f, indent=4)
    def to_jsons(self):
        return f'{{"id": "{self.id}", "name": "{self.name}"}}'
    def to_json(self):
        return json.loads(self.to_jsons())
    def from_json(json_obj):
        return user(json_obj.get("name"), id=json_obj.get("id"))

def load(id=None):
    if not os.path.exists("profiles.json"):
        with open("profiles.json", "w") as f:
            f.write('{"people": []}')
    data = {}
    with open("profiles.json", "r") as f:
        data = json.load(f)
    if id:
        return next((person for person in data.get("people") if person.get("id") == id), None)
    return data

global current_user
current_user = user("Public")