class DailyTarget:
    def __init__(self):
        self.protein = None
        self.carbs = None
        self.fats = None
        self.kcal = None

    def __repr__(self):
        return f"{self.__class__.__name__}(kcal = {self.kcal}, protein = {self.protein}, carbs = {self.carbs}, fats = {self.fats})"

    def create_daily_target(self, kcal: float, protein: float, carbs: float, fats: float) -> None:
        self.kcal= kcal
        self.protein = protein
        self.carbs = carbs
        self.fats = fats

    def set_daily_target(self, weight: float, height: float, activity: int, age: int, gender: "str") -> None:
        activity_list = [1.2, 1.375, 1.55, 1.725, 1.9]
        bmr = 0
        if gender == "male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == "female":
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        self.kcal = round(bmr * activity_list[activity - 1], -1)
        self.protein = self.kcal * 0.25
        self.carbs = self.kcal * 0.15
        self.fats = self.kcal * 0.6

if __name__ == "__main__":
    new_target = DailyTarget()
    print(new_target.set_daily_target(75, 182, 3, 16, "male"))
    print(new_target)
