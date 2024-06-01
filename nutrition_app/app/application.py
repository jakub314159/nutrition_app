import json
from base64 import b64encode, b64decode
from pathlib import Path
from random import choices, shuffle
from typing import Literal

from nutrition_app.error_station import error_base
from nutrition_app import logger
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.user.user import User

LOGIN_DIRPATH = Path(__file__).parent.parent / "user_base" / "login_base.json"
USER_DIRPATH = Path(__file__).parent.parent / "user_base" / "user_base.json"
CIFERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
LETTERS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "w",
    "x",
    "y",
    "z",
]
SPECIAL_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]


class UsernameTakenError(Exception):
    """
    Super class of "Exception", that pops up when the username is taken.
    """

    pass


class EmailTakenError(Exception):
    """
    Super class of "Exception", that pops up when the email is taken.
    """

    pass


class IncorrectLoginInformation(ValueError):
    """
    Super class of "ValueEror", that pops up when username or password are incorect while login in.
    """

    pass


class WrongMadePasswordError(ValueError):
    """
    Super class of "ValueEror", that pops up when the password is incorrectly made.
    """

    pass


class App:
    """
    This class is the application for counting your daily eating progres.

    Attributes:
        username: The username required to use the app.
        password: The password required to use the app.
        email: The email required to register to the app.
    """

    def __init__(self):
        self.username = None
        self.password = None
        self.email = None
        self.user = None

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @staticmethod
    def delete_account(index: int, dirpath: Path = None) -> None:
        """
        This lets the user delete the app from the user_base.
        Args:
            index: the number in the "users" dict that is needed to delete the account.
            dirpath: dirpath to the user_base is provided but can be changed for test purposes.
        """
        path = dirpath or LOGIN_DIRPATH
        with open(path, "r") as file:
            inside = json.load(file)
        inside["users"].pop(index)
        with open(path, "w") as file:
            json.dump(inside, file, indent=2)

    @staticmethod
    def check_password(password: str) -> str:
        if len(password) < 10 or len(password) > 20:
            raise WrongMadePasswordError("Password must have from 10 to 20 characters.")

        if password.isupper():
            raise WrongMadePasswordError("must have small leters")

        if password.islower():
            raise WrongMadePasswordError("must have big letters")

        if len([x for x in password if x.isnumeric()]) == 0:
            raise WrongMadePasswordError("must have a number")

        if len([x for x in password if x.isalnum() is False]) == 0:
            raise WrongMadePasswordError("must have a special character")

        if len([x for x in password if x.isnumeric() or x.isalnum() is False]) == len(password):
            raise WrongMadePasswordError("password must have a letter in it.")

        return password

    @staticmethod
    def automatic_password(
        upper_letters: int = None, lower_letters: int = None, numbers: int = None, special_char: int = None
    ):
        upp = [x.title() for x in choices(LETTERS, k=upper_letters)]
        low = choices(LETTERS, k=lower_letters)
        num = choices(CIFERS, k=numbers)
        char = choices(SPECIAL_CHARS, k=special_char)

        sum_list = upp + low + num + char

        if len(sum_list) < 10 or len(sum_list) > 20:
            raise WrongMadePasswordError("Password must have from 10 to 20 characters.")
        shuffle(x=sum_list)

        return "".join(sum_list)

    @classmethod
    def register(cls, username: str, password: str, email: str, dirpath: Path = None) -> None:
        """
        This lets the user set up a new account in the app.
        Args:
            username: The username required to use the app.
            password: The password required to use the app.
            email: The email required to register to the app.
            dirpath: dirpath to the user_base is provided but can be changed for test purposes.
        """
        cls.check_password(password)

        with open(dirpath or LOGIN_DIRPATH, "r") as file:
            inside = json.load(file)

        if username in [x["username"] for x in inside["users"]]:
            raise UsernameTakenError(error_base.get("E11").format(username))

        elif b64encode(email.encode("utf-8")).decode("utf-8") in [x["email"] for x in inside["users"]]:
            raise EmailTakenError(error_base.get("E11").format(email))

        inside["users"].append(
            {
                "username": username,
                "password": b64encode(password.encode("utf-8")).decode("utf-8"),
                "email": b64encode(email.encode("utf-8")).decode("utf-8"),
            }
        )
        with open(dirpath or LOGIN_DIRPATH, "w") as file:
            json.dump(inside, file, indent=2)

    def login(self, username, password, dirpath: Path = None):
        with open(dirpath or LOGIN_DIRPATH, "r") as file:
            inside = json.load(file)

        if (username, password) not in [
            (x["username"], b64decode(x["password"].encode("utf-8")).decode("utf-8")) for x in inside["users"]
        ]:
            raise IncorrectLoginInformation(error_base.get("E13"))

        self.username = username
        self.password = password
        self.load_user()

    def load_user(self):
        with open(USER_DIRPATH, "r") as file:
            inside = json.load(file)
        user_info = [(x["username"], x["user"]) for x in inside["users"] if self.username == x["username"]]
        if len(user_info) != 0:
            self.user = User.from_dict(user_info[0][1])
        else:
            logger.warning("User is not created, please create a new user, by calling 'create_user' method.")

    def reload_base(self, user_dict, filepath):
        with open(filepath or USER_DIRPATH, "r") as file:
            inside = json.load(file)
        inside["users"].append({"username": self.username, "user": user_dict})
        with open(filepath or USER_DIRPATH, "w") as file:
            json.dump(inside, file, indent=4)

    def create_user(
        self,
        name: str,
        surname: str,
        age: int,
        height: int,
        weight: int,
        gender: str,
        daily_target: DailyTarget,
        filepath=None,
    ):
        user = User(
            name=name, surname=surname, age=age, height=height, weight=weight, gender=gender, daily_target=daily_target
        )

        user_dict = user.to_dict()

        self.reload_base(user_dict, filepath or USER_DIRPATH)
        self.user = user

    def new_daily_target(
        self,
        kcal: float | None = None,
        protein: float | None = None,
        carbs: float | None = None,
        fats: float | None = None,
        activity: Literal["1", "2", "3", "4", "5"] | None = None,
    ):
        try:
            if kcal and protein and carbs and fats:
                self.user.create_daily_target(kcal, protein, carbs, fats)
            elif activity:
                self.user.set_daily_target(activity)
            else:
                logger.warning("Not enough data given, please give: kcal, protein, carbs, fats or activity.")
        except ValueError as e:
            logger.warning("daily target cannot be set due to %s", e)


app = App()
target = DailyTarget()
app.login("test1", "1234")
