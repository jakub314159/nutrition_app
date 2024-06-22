import json
import sqlite3
from base64 import b64encode, b64decode
from pathlib import Path
from random import choices, shuffle
from typing import Literal

from nutrition_app.error_station import error_base
from nutrition_app import logger, database_path
from nutrition_app.sql_connector import SQLConnector
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

    DATABASE_DIR = database_path

    def __init__(self, **kwargs):
        self._logins_name = "logins"
        self.username = None
        self.password = None
        self.email = None
        self.user = None
        self.database_connector = kwargs.pop("database_connector") or SQLConnector(self.DATABASE_DIR)

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def delete_account(self, table_name, primary_column, main_value) -> None:
        # TODO: type hints
        self.database_connector.remove_from_table(table_name, primary_column, main_value)

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
        # TODO: Handle automatic pass generator with no values given
        upp = [x.title() for x in choices(LETTERS, k=upper_letters)]
        low = choices(LETTERS, k=lower_letters)
        num = choices(CIFERS, k=numbers)
        char = choices(SPECIAL_CHARS, k=special_char)

        sum_list = upp + low + num + char

        if len(sum_list) < 10 or len(sum_list) > 20:
            raise WrongMadePasswordError("Password must have from 10 to 20 characters.")
        shuffle(x=sum_list)

        return "".join(sum_list)

    def _check_products_table(self) -> bool:
        tables = self.database_connector.get_existing_tables()
        return bool(tables) and self._logins_name in tables

    def _delete_products_table(self, name):
        self.database_connector.remove_table(name)

    def _create_products_table(self):
        if not self._check_products_table():
            self.database_connector.create_table(self._logins_name, ("username", "password", "email", "user"))

    def save_to_sql_db(self, username, password, email):
        self._create_products_table()
        self.database_connector.add_to_table(
            self._logins_name,
            [(username, password, email, None)],
        )

    def register(self, username: str, password: str, email: str) -> None:
        """
        This lets the user set up a new account in the app.
        Args:
            username: The username required to use the app.
            password: The password required to use the app.
            email: The email required to register to the app.
        """
        self.check_password(password)
        try:
            tables = self.database_connector.get_table(self._logins_name)
            if username in tables["username"]:
                raise UsernameTakenError(error_base.get("E11").format(username))

            elif email in tables["email"]:
                raise EmailTakenError(error_base.get("E11").format(email))

        except sqlite3.OperationalError:
            pass

        finally:
            self.save_to_sql_db(username, password, email)

    def login(self, username, password, dirpath: Path = None):
        # TODO: remove dirpath
        tables = self.database_connector.get_table(self._logins_name)
        print(tables)

        if username not in tables["username"] or password not in tables["password"] or tables["username"].index(username) != tables["password"].index(password):
            raise IncorrectLoginInformation(error_base.get("E13"))

        self.username = username
        self.password = password
        self.load_user()

    def load_user(self):
        # data = self.database_connector.get_record_from_table(self._logins_name, "username", self.username)
        # # TODO: create new table "users" and read User instance from it
        # if data["user"] is not None:
        #     self.user = data["user"]
        # else:
        #     logger.warning("User is not created, please create a new user, by calling 'create_user' method.")
        pass

    def update_record(self, key_name, new_val):
        self.database_connector.update_record_in_table(table_name=self._logins_name, primary_key_name="username", primary_key_val=self.username, key_name=key_name, new_value=new_val)

    def create_user(
        self,
        name: str,
        surname: str,
        age: int,
        height: int,
        weight: int,
        gender: str,
        daily_target: DailyTarget,
    ):
        user = User(
            name=name, surname=surname, age=age, height=height, weight=weight, gender=gender, daily_target=daily_target
        )

        self.update_record(user)
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
