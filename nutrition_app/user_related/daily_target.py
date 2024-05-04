from typing import Literal

from nutrition_app.constants import ACTIVITY_COEFFICIENTS, Gender



class DailyTarget:
    def __init__(self):
        self.protein = None
        self.carbs = None
        self.fats = None
        self.kcal = None

    def __repr__(self):
        return f"{self.__class__.__name__}(kcal = {self.kcal}, protein = {self.protein}, carbs = {self.carbs}, fats = {self.fats})"

    def create_daily_target(
        self, kcal: float, protein: float, carbs: float, fats: float
    ) -> None:
        self.kcal = kcal
        self.protein = protein
        self.carbs = carbs
        self.fats = fats

    def set_daily_target(
        self, weight: float, height: float, activity: Literal[1, 2, 3, 4, 5], age: int, gender: Literal["male", "female"] | str
    ) -> None:

        if activity not in ACTIVITY_COEFFICIENTS:
            raise ValueError("activity must be an integer in range 1 to 5")

        if gender == Gender.MALE:
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == Gender.FEMALE:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            raise ValueError("gender must be 'male' or 'female'")

        self.kcal = round(bmr * ACTIVITY_COEFFICIENTS[activity], -1)


        self.protein = self.kcal * 0.25
        self.carbs = self.kcal * 0.15
        self.fats = self.kcal * 0.6


if __name__ == "__main__":
    new_target = DailyTarget()
    print(new_target.set_daily_target(70, 170, 3, 18, "male"))
    print(new_target)
