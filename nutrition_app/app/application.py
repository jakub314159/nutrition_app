import random
from base64 import b64encode
from pathlib import Path
from random import choices, shuffle
from typing import Literal, Any, Sequence

from nutrition_app.error_station import error_base
from nutrition_app import logger, database_path
from nutrition_app.models.fast_product import FastProduct
from nutrition_app.models.product import EatableProduct
from nutrition_app.sql_connector import SQLConnector
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.user.user import User
from nutrition_app.email_sender.email_sender import Sender
from nutrition_app.work_flow.days_manager import DaysManager
from nutrition_app.products_base.products_base_manager import ProductsManager
from tests.mocked_connector import MockedConnector

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
    Super class of "ValueError", that pops up when username or password are incorrect while login in.
    """

    pass


class WrongMadePasswordError(ValueError):
    """
    Super class of "ValueError", that pops up when the password is incorrectly made.
    """

    pass


class App:
    """
    This class is the application for counting your daily eating progres.

    Attributes:
        _username: The username required to use the app.
    """

    DATABASE_DIR = database_path

    def __init__(self, **kwargs):
        self._logins_name = "logins"
        self._users_name = "users"
        self._verification_name = "verification"
        self._daily_target_name = "target"
        self._username: str | None = None
        self._user: User | None = None
        self.database_connector = kwargs.get("database_connector") or SQLConnector(self.DATABASE_DIR)
        logger.info(f"creating database {self.DATABASE_DIR}")
        self.days_manager: DaysManager | MockedConnector | None = None
        self.id_base_manager = ProductsManager()

        self._create_table(self._logins_name, ("username", "password", "email", "verified"))
        self._create_table(self._users_name, ("username", "name", "surname", "age", "height", "weight", "gender"))
        self._create_table(self._verification_name, ("email", "code"))
        self._create_table(self._daily_target_name, ("username", "protein", "carbs", "fats", "kcal"))

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @staticmethod
    def check_password(password: str) -> str:
        """
        Check if your password meets the requirements.

        Args:
            password(str): The password that is going to be checked.

        Raises:
            WrongMadePasswordError:
                password isn't from 8 - 20 characters.
                doesn't have small letters.
                doesn't have big letters.
                doesn't have numbers.
                doesn't have special characters.
                doesn't have letters.

        Returns:
            str: password if it's correct.
        """
        if len(password) < 8 or len(password) > 20:
            raise WrongMadePasswordError("Password must have from 8 to 20 characters.")

        if password.isupper():
            raise WrongMadePasswordError("must have small letters")

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
    def automatic_password() -> str:
        """
        Creates an automatic password.

        Returns:
            str: password if the user doesn't provide one.
        """

        upp = [x.title() for x in choices(LETTERS, k=random.randint(2, 5))]
        low = choices(LETTERS, k=random.randint(2, 5))
        num = choices(CIFERS, k=random.randint(2, 5))
        char = choices(SPECIAL_CHARS, k=random.randint(2, 5))

        sum_list = upp + low + num + char
        shuffle(x=sum_list)

        return "".join(sum_list)

    def _create_table(self, table_name: str, fields: Sequence[str]) -> None:
        """
        Creates a products table if the table doesn't exist.

        Args:
            table_name(str): the name of the table.
            fields(Sequence[str]): the fields in the table.

        Returns:
            None
        """
        self.database_connector.create_table(table_name, fields)

    def _update_record(self, key_name: str, new_val: Any) -> None:
        """
        Update record in the database.

        Args:
            key_name(str): the column in which the value is updated.
            new_val(Any): new value in the column.

        Returns:
            None
        """
        self.database_connector.update_record_in_table(
            table_name=self._logins_name,
            primary_key_name="username",
            primary_key_val=self._username,
            key_name=key_name,
            new_value=new_val,
        )

    def _save_to_logins_db(self, username: str, password: str, email: str) -> None:
        """
        Saves user information to the database.

        Args:
            username(str): username required to use the app.
            password(str): users password.
            email(str): users email.

        Returns:
            None
        """
        self.database_connector.add_to_table(
            self._logins_name,
            [
                (
                    username,
                    b64encode(password.encode("utf-8")).decode("utf-8"),
                    b64encode(email.encode("utf-8")).decode("utf-8"),
                    False,
                )
            ],
        )

    def register(self, username: str, password: str, email: str) -> None:
        """
        Set up a new account in the app.

        Args:
            username(str): username required to use the app.
            password(str): users password.
            email(str): users email.

        Returns:
            None
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

    def verify(self, username: str, email: str, code: str | int) -> None:
        """
        Verify your email in the app.

        Args:
            username(str): username required to use the app.
            email(str): users email.
            code(str | int): code required to verify.

        Raises:
            ValueError: if the code is wrong.

        Returns:
            None
        """

        if str(code) == self.database_connector.get_record_from_table(self._verification_name, "email", email)["code"]:
            self.database_connector.update_record_in_table(self._logins_name, "username", username, "verified", True)
            logger.info("Your email is now verified.")
            self.database_connector.remove_from_table(
                table_name=self._verification_name, column_name="email", value=email
            )

        else:
            raise ValueError(error_base.get("E14"))

    def login(self, username: str, password: str) -> None:
        """
        Log to the application.

        Args:
            username(str): username required to use the app.
            password(str): users password.

        Raises:
            IncorrectLoginInformation: username or password is wrong.

        Warnings:
            if the email is not verified.

        Returns:
            None
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
            logger.warning("You need to verify your email first.")
            return None

        self._username = username
        self.load_user(username)

    def load_user(self, username: str) -> None:
        """
        Load user into the app from database.

        Args:
            username(str): username required to use the app.

        Returns:
            None
        """
        user_info = self.database_connector.get_record_from_table(
            table_name=self._users_name, key_name="username", key_val=username
        )

        if user_info != {}:
            username = user_info.pop("username")

            dict_dt = self.database_connector.get_record_from_table(
                table_name=self._daily_target_name, key_name="username", key_val=username
            )
            if dict_dt != {}:
                dict_dt.pop("username")
                daily_target = DailyTarget.from_dict(dict_dt)
                user_info["daily_target"] = daily_target
            else:
                logger.info("Please create daily_target with create_daily_target method.")

            logger.info("User is loaded.")
            user = User.from_dict(user_info)
            self._user = user
            if self.database_connector == MockedConnector():
                self.days_manager = DaysManager(username=username, user=self._user, connector=MockedConnector())
            self.days_manager = DaysManager(username=username, user=self._user)

        else:
            logger.info("Please create a new user with create_user method.")

    def create_user(
        self,
        name: str,
        surname: str,
        age: int,
        height: int,
        weight: int,
        gender: str,
        daily_target: DailyTarget = None,
    ) -> None:
        """
        Creates a user representation in the app.

        Args:
            name(str): the name of the user.
            surname(str): the surname of the user.
            age(int): the age of the user.
            height(int): the height of the user.
            weight(int): the weight of the user.
            gender(str): the gender of the user.
            daily_target(DailyTarget): object of class daily_target.

        Returns:
            None
        """
        user = User(
            name=name, surname=surname, age=age, height=height, weight=weight, gender=gender, daily_target=daily_target
        )

        if not daily_target:
            logger.info(
                msg="Daily target not provided, please use create_daily_target method to set your daily target."
            )
        else:
            self.database_connector.add_to_table(
                self._daily_target_name,
                [(self._username, daily_target.protein, daily_target.carbs, daily_target.fats, daily_target.kcal)],
            )

        self.database_connector.add_to_table(
            self._users_name,
            [(self._username, user.name, user.surname, user.age, user.height, user.weight, user.gender)],
        )

        logger.info(msg="User created successfully.")
        self._user = user
        if self.database_connector == MockedConnector():
            self.days_manager = DaysManager(username=self._username, user=self._user, connector=MockedConnector())
        self.days_manager = DaysManager(username=self._username, user=self._user)

    def create_daily_target(
        self,
        kcal: float | None = None,
        protein: float | None = None,
        carbs: float | None = None,
        fats: float | None = None,
        activity: Literal[1, 2, 3, 4, 5] | None = 3,
    ) -> None:
        """
        Create a daily target for the user.

        Args:
            kcal(float): kcal required to create a table.
            protein(float): protein required to create a table.
            carbs(float): carbs required to create a table.
            fats(float): kcal required to create a table.
            activity(Literal[1,2,3,4,5]): kcal required to set the table.

        Warnings:
            if not enough data is given.

        Returns:
            None
        """
        try:
            if kcal and protein and carbs and fats:
                self._user.create_daily_target(kcal, protein, carbs, fats)
            else:
                self._user.set_daily_target(activity)
            logger.info(msg="Daily target created successfully.")
            self.database_connector.add_to_table(
                self._daily_target_name,
                [
                    (
                        self._username,
                        self._user.daily_target.protein,
                        self._user.daily_target.carbs,
                        self._user.daily_target.fats,
                        self._user.daily_target.kcal,
                    )
                ],
            )
        except ValueError as e:
            logger.warning("daily target cannot be set due to %s", e)

    def add_day(self, date: int) -> None:
        """
        Create a new eating_day for the user.

        Returns:
            None
        """
        self.days_manager.add_day(date)
        logger.info("Day added.")

    def add_products_to_meal(self, index: int, products: list[EatableProduct | FastProduct]) -> None:
        """
        Add products to meals in the eating_day.

        Args:
            index(int): the index of the users meal_order.
            products(list[EatableProduct | FastProduct]): products added to meal.

        Returns:
            None
        """
        self.days_manager.add_to_meal(index, products)
        logger.info("Products added to meal.")

    def add_product_by_id_to_meal(self, index: int, id_: int, mass: int) -> None:
        """
        Add product to meals in the eating_day by its id.

        Args:
            index(int): the index of the users meal_order.
            id_: the products id.
            mass: the products mass.

        Returns:
            None
        """
        product = self.id_base_manager.get_product_by_id(id_)
        e_product = EatableProduct(mass, product)
        self.days_manager.add_to_meal(index, [e_product])
        logger.info("Product added to meal.")

    def add_product_by_name_to_meal(self, index: int, name: str, mass: int) -> None:
        """
        Add product to meals in the eating_day by its name.

        Args:
            index(int): the index of the users meal_order.
            name: the products name.
            mass: the products mass.

        Returns:
            None
        """
        product = self.id_base_manager.get_product_by_name(name)
        e_product = EatableProduct(mass, product)
        self.days_manager.add_to_meal(index, [e_product])
        logger.info("Product added to meal.")

    def get_progress(self, variable: Literal["kcal", "protein", "carbs", "fats"] | None = None) -> float | None:
        """
        Get progress bar containing the amount of micronutrient consumed, users target and the progress percentage.

        Args:
            variable(Literal["kcal", "protein", "carbs", "fats"] | None): variable you use to see the progress bar.

        Returns:
            float | None: if the user chooses one variable it returns the amount of micronutrient consumed.
        """
        if self.days_manager is None:
            logger.warning("You need to create a day before getting progress.")

        else:
            if variable:
                print(self.days_manager.get_progress(variable)[0])
                return self.days_manager.get_progress(variable)[1]
            else:
                [print(self.days_manager.get_progress(x)[0]) for x in ["kcal", "protein", "carbs", "fats"]]

    def save_day(self, date: int) -> None:
        """
        Save any day to sql database.

        Args:
            date(int): the yy:mm:dd representation of the date.

        Returns:
            None
        """
        self.days_manager.save_to_database(date)
