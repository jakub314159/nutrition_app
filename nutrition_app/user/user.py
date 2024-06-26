from typing import Literal

from nutrition_app.sql_connector import SQLConnector
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.numerical_attribute import NumericalAttribute
from nutrition_app import database_path


class User:
    """
    This is the user representation.

    Attributes:
        name: users name.
        surname: users surname.
        age: users age (must be greater than 0).
        height: users height that will be turn into meters.
        weight: users weight.
        gender: users gender (male or female).
        daily_target: is an instance of the class DailyTarget, basic value is 0.
        meal_order: this is the order in which the user will eat his meals.
    """

    age = NumericalAttribute()
    height = NumericalAttribute()
    weight = NumericalAttribute()
    PRODUCTS_DIR = database_path
    TABLE_NAME = "users"

    def __init__(
        self,
        name: str,
        surname: str,
        age: int,
        height: float,
        weight: float,
        gender: str,
        daily_target: DailyTarget = None,
    ):
        self.name = name
        self.surname = surname
        self.age = age
        self.height = height if height > 2.5 else height * 100
        self.weight = weight
        self.gender = gender
        self.daily_target = daily_target or DailyTarget()
        self.meal_order = None or ["breakfast", "dinner", "snack", "supper"]

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, surname={self.surname}, weight={self.weight}, height={self.height}, age={self.age}, gender={self.gender}, daily_target={self.daily_target}, meal_order={self.meal_order})"

    def __eq__(self, other: "User"):
        if self.name == other.name and self.surname == other.surname and self.age == other.age:
            return True
        return False

    def count_bmi(self) -> float:
        """
        This will count the users bmi.
        Returns:
            user bmi.
        """
        height = self.height / 100
        return round(self.weight / height**2, 2)

    def create_daily_target(
        self,
        kcal: float,
        protein: float,
        carbs: float,
        fats: float,
    ) -> None:
        """
        This lets user create a daily target.
        Args:
            kcal: the amount of kcal needed to be consumed daily.
            protein: the amount of protein needed to be consumed daily.
            carbs: the amount of carbs needed to be consumed daily.
            fats: the amount of fats needed to be consumed daily.
        """
        self.daily_target.create_daily_target(kcal=kcal, protein=protein, carbs=carbs, fats=fats)

    def set_daily_target(self, activity: Literal[1, 2, 3, 4, 5]):
        """
        This lets user set a daily target based on his measurements and activity.
        Args:
            activity: users activity ranging from 1 to 5.
        """
        self.daily_target.set_daily_target(
            weight=self.weight,
            height=self.height,
            activity=activity,
            age=self.age,
            gender=self.gender,
        )

    def set_meal_order(self, meals: list[str]) -> None:
        """
        This lets the user set the meal order.
        Args:
            meals: list[str] the order of meals.
        """
        self.meal_order = meals

    def to_dict(self):
        """
        Returns: The users dict
        """
        user_dict = self.__dict__
        user_dict["daily_target"] = self.daily_target.to_dict()
        return user_dict

    @classmethod
    def from_dict(cls, data: dict[str]) -> "User":
        """
        This creates a new object of the class from dict.
        Args:
            data: The dict from wchih the new objewct will be created.

        Returns: The new object from data.
        """
        return cls(
            name=data["name"],
            surname=data["surname"],
            age=data["age"],
            height=data["height"],
            weight=data["weight"],
            gender=data["gender"],
            daily_target=DailyTarget.from_dict(data["daily_target"]),
        )

    # @classmethod
    # def _check_products_table(cls) -> bool:
    #     connector = SQLConnector(database_path=cls.PRODUCTS_DIR)
    #     tables = connector.get_existing_tables()
    #     return bool(tables) and cls.TABLE_NAME in tables
    #
    # def _create_products_table(self):
    #     if not self._check_products_table():
    #         connector = SQLConnector(database_path=self.PRODUCTS_DIR)
    #         connector.create_table(
    #             self.TABLE_NAME, ("name", "surname", "age", "height", "weight", "gender", "daily_target", "meal_order")
    #         )
    #
    # def save_to_sql_db(self):
    #     self._create_products_table()
    #     connector = SQLConnector(database_path=self.PRODUCTS_DIR)
    #     connector.add_to_table(
    #         self.TABLE_NAME,
    #         [
    #             (
    #                 self.name,
    #                 self.surname,
    #                 self.age,
    #                 self.height,
    #                 self.weight,
    #                 self.gender,
    #                 self.daily_target,
    #                 self.meal_order,
    #             )
    #         ],
    #     )
    #
    # @classmethod
    # def from_sql_db(cls, id_: int) -> dict:
    #     connector = SQLConnector(database_path=database_path)
    #     record = connector.get_record_from_table(cls.TABLE_NAME, "id", id_)
    #     return record
