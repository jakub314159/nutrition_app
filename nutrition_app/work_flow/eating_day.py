from nutrition_app.models.fast_product import FastProduct
from nutrition_app.models.meal import Meal
from nutrition_app.user_related.user import User
from nutrition_app.user_related.daily_target import DailyTarget
from nutrition_app.models.product import EatableProduct, Product
from nutrition_app.error_station import error_base




class Day:
    def __init__(self, user: User | str):
        self.user = user
        self.meals: dict[str, Meal] = {meal_name: Meal() for meal_name in self.user.meal_order}
        self.progres = {}

    def _validate(self, meal_index) -> None:
        if meal_index >= len(self.user.meal_order):
            raise ValueError(error_base.get("Error_10").format(len(user.meal_order) - 1))


    def add_to_meal(self, meal_index: int, products: list[EatableProduct | FastProduct]) -> None:
        self._validate(meal_index=meal_index)
        for product in products:
            self.meals[self.user.meal_order[meal_index]].add_product(product)

    def delete_from_meal(self, meal_index: int, product_index: int):
        self._validate(meal_index=meal_index)
        self.meals[self.user.meal_order[meal_index]].delete_product(product_index)

    @property
    def kcal_progres(self):
        self.progres["kcal"] = round(sum([x.count_ov_kcal() for x in self.meals.values()]) / self.user.daily_target.kcal)
        return self.progres["kcal"]
    @property
    def protein_progres(self):
        self.progres["protein"] = round(sum([x.count_ov_protein() for x in self.meals.values()]) / self.user.daily_target.protein)
        return self.progres["protein"]

    @property
    def carbs_progres(self):
        self.progres["carbs"] = round(sum([x.count_ov_carbs() for x in self.meals.values()]) / self.user.daily_target.carbs)
        return self.progres["carbs"]

    @property
    def fats_progres(self):
        self.progres["fats"] = round(sum([x.count_ov_fats() for x in self.meals.values()]) / self.user.daily_target.fats)
        return self.progres["fats"]

if __name__ == "__main__":
    product_list = [EatableProduct(mass= 100, product=Product("masło", 10, 15, 30, 40, 34)), EatableProduct(mass= 100, product=Product("ser", 10, 10, 30, 40, 34))]
    meals_dict = {"breakfast": Meal(product_list)}
    user = User(
        name="Jan", surname="Kowalski", weight=70, height=170, age=18, gender="male"
    )
    user.set_daily_target(activity=3)

    new_day = Day(meals=meals_dict, user=user)
    print(new_day.list_progres())

