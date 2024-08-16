from typing import Literal

from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.numerical_attribute import NumericalAttribute
from nutrition_app import logger, database_path


class User:
    """
    This is the user representation.

    Attributes:
        name(str): users name.
        surname(str): users surname.
        age(int): users age (must be greater than 0).
        height(float): users height that will be turn into meters.
        weight(float): users weight.
        gender(str): users gender (male or female).
        daily_target(DailyTarget): is an instance of the class DailyTarget, basic value is 0.
        meal_order(None | list[str]): this is the order in which the user will eat his meals.
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
        self.meal_order: None | list[str] = None or ["breakfast", "dinner", "snack", "supper"]

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, surname={self.surname}, weight={self.weight}, height={self.height}, age={self.age}, gender={self.gender}, daily_target={self.daily_target}, meal_order={self.meal_order})"

    def __eq__(self, other: "User"):
        if self.name == other.name and self.surname == other.surname and self.age == other.age:
            return True
        return False

    def count_bmi(self) -> float:
        """
        Count the users bmi.

        Returns:
            float: users bmi.
        """
        height = self.height / 100
        return round(self.weight / height**2, 2)

    def create_daily_target(
        self, kcal: float, protein: float, carbs: float, fats: float, goal: bool | None = None
    ) -> None:
        """
        Create a daily target for the user.

        Args:
            kcal(float): the amount of kcal needed to be consumed daily.
            protein(float): the amount of protein needed to be consumed daily.
            carbs(float): the amount of carbs needed to be consumed daily.
            fats(float): the amount of fats needed to be consumed daily.

        Returns:
            None
        """
        self.daily_target.create_daily_target(kcal=kcal, protein=protein, carbs=carbs, fats=fats)

    def set_daily_target(self, activity: Literal[1, 2, 3, 4, 5]) -> None:
        """
        Set a daily target based on users activity.

        Args:
            activity(Literal[1, 2, 3, 4, 5]): users activity ranging from 1 to 5.

        Returns:
            None
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
        Set the meal order.

        Args:
            meals (list[str]): the order of meals.

        Returns:
            None
        """
        logger.info("Meal order created successfully.")
        self.meal_order = meals

    def to_dict(self) -> dict:
        """
        Returns:
            dict: user dict.
        """
        user_dict = self.__dict__
        user_dict["daily_target"] = self.daily_target.to_dict()
        return user_dict

    @classmethod
    def from_dict(cls, data: dict[str]) -> "User":
        """
        Creates a User object from dict.

        Args:
            data (dict[str]): the dict from which the User will be created.

        Returns:
            User: new object from the class User.
        """
        daily_target = data.pop("daily_target", None)

        return cls(
            name=data["name"],
            surname=data["surname"],
            age=data["age"],
            height=data["height"],
            weight=data["weight"],
            gender=data["gender"],
            daily_target=daily_target,
        )
