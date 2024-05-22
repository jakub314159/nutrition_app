import json
from pathlib import Path

from nutrition_app.user.user import User

DIRPATH = Path(__file__).parent.parent / "user_base" / "user_base.json"

class App:
    def __init__(self):
        self.username = None
        self.password = None
        self.email = None

    def register(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email



        with open(DIRPATH, "r") as file:
            inside = json.load(file)
        inside["users"].append({username: password})
        with open(DIRPATH, "w") as file:
            json.dump(inside, file, indent= 4)