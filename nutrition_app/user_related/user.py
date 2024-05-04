from nutrition_app.user_related.daily_target import DailyTarget
from nutrition_app.numerical_attribute import NumericalAttribute


class User:

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
        self.height = height
        self.weight = weight
        self.gender = gender
        self.daily_target = DailyTarget() or daily_target

    def count_bmi(self) -> float:
        height = self.height / 100
        return round(self.weight / height ** 2, 2)

    def create_daily_target(
        self,
        kcal: float,
        protein: float = None,
        carbs: float = None,
        fats: float = None,
    ):
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


if __name__ == "__main__":
    new_user = User(
        name="Jan", surname="Kowalski", age=20, height=180, weight=70, gender="male"
    )
    print(new_user.count_bmi())
    new_user.create_daily_target(kcal=3000, protein=200, carbs=350)
    print(new_user.daily_target)
