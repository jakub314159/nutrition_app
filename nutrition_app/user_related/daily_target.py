from typing import Literal

from nutrition_app.constants import ACTIVITY_COEFFICIENTS, Gender
from nutrition_app.error_station import error_base


class IncorrectMacroError(ValueError):
    """This error will pop up if macro input is not adding up."""

    pass


class DailyTarget:
    """
    This class lets you set or create a target for the user.

    Attributes:
        protein: the ammount od protein
        carbs: the ammount od carbs
        fats: the ammount od fats
        kcal: the ammount od kcal
    """

    def __init__(self):
        self.protein = None
        self.carbs = None
        self.fats = None
        self.kcal = None

    def __repr__(self):
        return f"{self.__class__.__name__}(kcal={self.kcal}, protein={self.protein}, carbs={self.carbs}, fats={self.fats})"

    def create_daily_target(
        self, kcal: float, protein: float, carbs: float, fats: float
    ) -> None:
        """
        This lets you create a daily target.

        Args:
            kcal: the amount of calories.
            protein: the amount of protein.
            carbs: the amount of carbs.
            fats: the amount of fats.
        Raises:
            IncorrectMacroError (super class of ValueError): if the usser input is wrong.
        """

        if not round(protein * 4 + carbs * 4 + fats * 9) == round(kcal):
            raise IncorrectMacroError(error_base.get("E5"))

        self.kcal = kcal
        self.protein = protein
        self.carbs = carbs
        self.fats = fats

    def set_daily_target(
        self,
        weight: float,
        height: float,
        activity: Literal[1, 2, 3, 4, 5],
        age: int,
        gender: Literal["male", "female"] | str,
    ) -> None:
        """
        This lets you set a daily target.
        Args:
            weight: the users weight.
            height: the users height.
            activity: the users level of activity reaching from 1 (the lowest) to 5 (the highest).
            age: users age.
            gender: users gender (male or female).
        Raises:
            ValueError: when activity doesn't belong into 1 - 5 range and when gender is not male or female.
        """

        if activity not in ACTIVITY_COEFFICIENTS:
            raise ValueError(error_base.get("E6"))

        if gender == Gender.MALE:
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == Gender.FEMALE:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            raise ValueError(error_base.get("E7"))

        self.kcal = round(bmr * ACTIVITY_COEFFICIENTS[activity], -1)

        self.protein = self.kcal * 0.20 / 4
        self.carbs = self.kcal * 0.50 / 4
        self.fats = self.kcal * 0.30 / 9

    def to_dict(self):
        return self.__dict__


if __name__ == "__main__":
    new_target = DailyTarget()
    print(new_target.set_daily_target(70, 170, 3, 18, "male"))
    print(new_target)
