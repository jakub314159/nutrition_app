from nutrition_app.user_related.daily_target import DailyTarget
from nutrition_app.numerical_attribute import NumericalAttribute


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
    """
    age = NumericalAttribute()
    height = NumericalAttribute()
    weight = NumericalAttribute()

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
        self.daily_target = DailyTarget() or daily_target
        self.meal_order = None or ["breakfast", "dinner", "snack", "supper"]

    def count_bmi(self) -> float:
        """
        This will count the users bmi.
        Returns:
            user bmi
        """
        height = self.height / 100
        return round(self.weight / height ** 2, 2)

    def create_daily_target(
        self,
        kcal: float,
        protein: float = None,
        carbs: float = None,
        fats: float = None,
    ) -> None:
        """
        This lets user create a daily target
        Args:
            kcal: the amount of kcal needed to be consumed daily
            protein:
            carbs:
            fats:
        """
        self.daily_target.create_daily_target(
            kcal=kcal, protein=protein, carbs=carbs, fats=fats
        )

    def set_daily_target(self, activity):
        self.daily_target.set_daily_target(
            weight=self.weight,
            height=self.height,
            activity=activity,
            age=self.age,
            gender=self.gender,
        )

    def set_meal_order(self, meals:list[str]) -> None:
        self.meal_order = meals
