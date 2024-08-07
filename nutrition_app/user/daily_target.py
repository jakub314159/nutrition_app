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
        protein(float): the amount od protein
        carbs(float): the amount od carbs
        fats(float): the amount od fats
        kcal(float): the amount od kcal
    """

    def __init__(
        self,
        protein: float | None = None,
        carbs: float | None = None,
        fats: float | None = None,
        kcal: float | None = None,
    ):
        self._validate_macro(protein, carbs, fats, kcal)
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.kcal = kcal

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(kcal={self.kcal}, protein={self.protein}, carbs={self.carbs}, fats={self.fats})"
        )

    def __eq__(self, other):
        if (
            self.kcal == other.kcal
            and self.protein == other.protein
            and self.carbs == other.carbs
            and self.fats == other.fats
        ):
            return True
        return False

    @staticmethod
    def _validate_macro(protein, carbs, fats, kcal) -> None:
        """
        This validates if the macro input is correct.

        Args:
            protein(float): the amount od protein
            carbs(float): the amount od carbs
            fats(float): the amount od fats
            kcal(float): the amount od kcal

        Returns:
            None
        """
        if protein or carbs or fats or kcal:
            if not round(protein * 4 + carbs * 4 + fats * 9) == round(kcal):
                raise IncorrectMacroError(error_base.get("E5"))

    def create_daily_target(self, kcal: float, protein: float, carbs: float, fats: float) -> None:
        """
        Create a daily target.

        Args:
            kcal(float): the amount of calories.
            protein(float): the amount of protein.
            carbs(float): the amount of carbs.
            fats(float): the amount of fats.

        Raises:
            IncorrectMacroError(ValueError): if the user input is wrong.

        Returns:
            None
        """
        self._validate_macro(protein, carbs, fats, kcal)

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
            weight(float): the users weight.
            height(float): the users height.
            activity(Literal[1, 2, 3, 4, 5]): the users level of activity reaching from 1 (the lowest) to 5 (the highest).
            age(float): users age.
            gender(Literal["male", "female"] | str): users gender (male or female).

        Raises:
            ValueError: when activity doesn't belong into 1 - 5 range and when gender is not male or female.

        Returns:
            None
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

        self.protein = round(self.kcal * 0.20 / 4, 2)
        self.carbs = round(self.kcal * 0.50 / 4, 2)
        self.fats = round(self.kcal * 0.30 / 9, 2)

    def to_dict(self) -> dict:
        """
        Returns:
            dict: daily target dict.
        """
        return self.__dict__

    @classmethod
    def from_dict(cls, daily_target_dict: dict[str]) -> "DailyTarget":
        """
        Creates a DailyTarget object from dict.

        Args:
            daily_target_dict (dict[str]): the dict from which the new object will be created.

        Returns:
            DailyTarget: new object from the class DailyTarget.
        """
        return cls(**daily_target_dict)
