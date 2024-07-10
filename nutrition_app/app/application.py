import json
import random
import sqlite3
from base64 import b64encode, b64decode
from pathlib import Path
from random import choices, shuffle
from typing import Literal, Any, Sequence

from nutrition_app.error_station import error_base
from nutrition_app import logger, database_path
from nutrition_app.sql_connector import SQLConnector
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.user.user import User
from nutrition_app.email_sender.email_sender import Sender

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
        self._users_name = "users"
        self._verification_name = "verification"
        self.username = None
        self.password = None
        self.email = None
        self.user = None
        self.database_connector = kwargs.get("database_connector") or SQLConnector(self.DATABASE_DIR)
        logger.info(f"creating database {self.DATABASE_DIR}")

        self._create_table(self._logins_name, ("username", "password", "email", "verified"))
        self._create_table(
            self._users_name, ("username", "name", "surname", "age", "height", "weight", "gender", "daily_target"))
        self._create_table(self._verification_name, ("email", "code"))

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def delete_account(self, table_name: str, primary_column: str, primary_value: Any) -> None:
        """
        Args:
            table_name: the name of the table from wchih you delete an account.
            primary_column: the main column name.
            primary_value: the main column value.
        """
        self.database_connector.remove_from_table(table_name, primary_column, primary_value)

    @staticmethod
    def check_password(password: str) -> str:
        """
        Args:
            password: The password that is going to be checked.

        Raises:
            WrongMadePasswordError:
                password isn't from 8 - 20 characters.
                doesn't have small letters.
                doesn't have big letters.
                doesn't have numbers.
                doesn't have special characters.
                doesn't have letters.

        Returns:
            The password if it's correct.
        """
        if len(password) < 8 or len(password) > 20:
            raise WrongMadePasswordError("Password must have from 8 to 20 characters.")

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
    def automatic_password():
        """
        Returns:
            Password if the user doesn't provide one.
        """

        upp = [x.title() for x in choices(LETTERS, k=random.randint(2, 5))]
        low = choices(LETTERS, k=random.randint(2, 5))
        num = choices(CIFERS, k=random.randint(2, 5))
        char = choices(SPECIAL_CHARS, k=random.randint(2, 5))

        sum_list = upp + low + num + char
        shuffle(x=sum_list)

        return "".join(sum_list)

    def _check_table(self, table_name: str) -> bool:
        """
        This checks if the products table exists.

        Returns:
            a True or False statement if the products table exists.
        """
        tables = self.database_connector.get_existing_tables()
        return bool(tables) and table_name in tables

    def _delete_table(self, name: str):
        """
        This deletes the products table.
        Args:
            name: The name of the table.
        """
        self.database_connector.remove_table(name)

    def _create_table(self, table_name: str, fields: Sequence[str]):
        """
        This creates a products table if the table doesn't exist.
        """
        if not self._check_table(table_name):
            self.database_connector.create_table(table_name, fields)

    def _update_record(self, key_name: str, new_val: Any):
        """
        This updates record in the database.
        Args:
            key_name: the column in which the value is updated.
            new_val: new value in the column.
        """
        self.database_connector.update_record_in_table(
            table_name=self._logins_name,
            primary_key_name="username",
            primary_key_val=self.username,
            key_name=key_name,
            new_value=new_val,
        )

    def _save_to_logins_db(self, username: str, password: str, email: str):
        """
        This saves user information to the database.
        Args:
            username: The username required to use the app.
            password: Users password.
            email: Users email.
        """
        self.database_connector.add_to_table(
            self._logins_name,
            [
                (
                    username,
                    b64encode(password.encode("utf-8")).decode("utf-8"),
                    b64encode(email.encode("utf-8")).decode("utf-8"),
                    False
                )
            ],
        )

    def register(self, username: str, password: str, email: str) -> None:
        """
        This lets the user set up a new account in the app.
        Args:
            username: The username required to use the app.
            password: Users password.
            email: Users email.
        """
        self.check_password(password)


        tables = self.database_connector.get_table(self._logins_name)
        if username in tables["username"]:
            raise UsernameTakenError(error_base.get("E11").format(username))

        elif b64encode(email.encode("utf-8")).decode("utf-8") in tables["email"]:
            raise EmailTakenError(error_base.get("E11").format(email))

        verification = Sender(email)
        code = verification.send_verification_message()

        self.database_connector.add_to_table(self._verification_name, [(email, code)])
        self._save_to_logins_db(username, password, email)

    def verify(self, username: str, email: str, code: str):
        if code == self.database_connector.get_record_from_table(self._verification_name, "email", email)["code"]:
            self.database_connector.update_record_in_table(self._logins_name, "username", username, "verified", True)
        else:
            raise ValueError(error_base.get("E14"))

    def login(self, username: str, password: str):
        """
        This lets the user log to the application
        Args:
            username: The username required to use the app.
            password: Users password.
        Raises:
            IncorrectLoginInformation:
                username or password is wrong.
        """
        tables = self.database_connector.get_table(self._logins_name)

        if (
            username not in tables["username"]
            or b64encode(password.encode("utf-8")).decode("utf-8") not in tables["password"]
            or tables["username"].index(username)
            != tables["password"].index(b64encode(password.encode("utf-8")).decode("utf-8"))
        ):
            raise IncorrectLoginInformation(error_base.get("E13"))

        if not self.database_connector.get_record_from_table(self._logins_name, "username", username)["verified"]:
            logger.warning("You need to verify your email first")
            return None

        self.username = username
        self.password = password
        self.load_user()

    def load_user(self, user: "User" = None):
        """
        This lets app user to load their user profile.
        Args:
            user: the user needed to use the app.
        Warnings:
            if user hasn't been created.
        """

        if self.user is not None:
            self.database_connector.add_to_table(
                self._users_name,
                [
                    (
                        self.username,
                        self.user.name,
                        self.user.surname,
                        self.user.age,
                        self.user.height,
                        self.user.weight,
                        self.user.gender,
                        self.user.daily_target,
                    )
                ],
            )
        elif self.user is None and user is not None:
            self.database_connector.add_to_table(
                self._users_name,
                [
                    (
                        self.username,
                        user.name,
                        user.surname,
                        user.age,
                        user.height,
                        user.weight,
                        user.gender,
                        user.daily_target,
                    )
                ],
            )
        else:
            logger.info(msg="insufficient information, please create a new user.")

    def create_user(
        self,
        name: str,
        surname: str,
        age: int,
        height: int,
        weight: int,
        gender: str,
        daily_target: DailyTarget = None,
    ):
        user = User(
            name=name, surname=surname, age=age, height=height, weight=weight, gender=gender, daily_target=daily_target
        )

        self.load_user(user)
        self.user = user

    def create_daily_target(
        self,
        kcal: float | None = None,
        protein: float | None = None,
        carbs: float | None = None,
        fats: float | None = None,
        activity: Literal[1, 2, 3, 4, 5] | None = None,
    ):
        """
        This lets the user create a new daily target.
        Args:
            kcal: kcal required to create a table.
            protein: protein required to create a table.
            carbs: carbs required to create a table.
            fats: kcal required to create a table.
            activity: kcal required to set the table.

        Warnings:
            if not enough data is given.

        """
        try:
            if kcal and protein and carbs and fats:
                self.user.create_daily_target(kcal, protein, carbs, fats)
            elif activity:
                self.user.set_daily_target(activity)
            else:
                logger.warning("Not enough data given, please give: kcal, protein, carbs, fats or activity.")
        except ValueError as e:
            logger.warning("daily target cannot be set due to %s", e)

if __name__ == "__main__":
    app = App()
    app.register("user", "pass1234G*", "email")
    app.login("user", "pass1234G*")
    app.verify("user", "email", )