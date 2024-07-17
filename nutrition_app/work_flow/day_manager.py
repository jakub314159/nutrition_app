from typing import Sequence, TypedDict, Literal

from nutrition_app.models.product import EatableProduct, Product
from nutrition_app.user.user import User
from nutrition_app.work_flow.eating_day import Day


class DaysManager:
    def __init__(self, user: User):
        self.days: list[Day] = []
        self.meal_order = user.meal_order
        self.user = user

    def add_day(self):
        day = Day(user=self.user)
        self.days.append(day)

    def add_to_meal(self, index: int, products: list[EatableProduct | Product]):
        for product in products:
            self.days[-1].meals[self.meal_order[index]].add_product(product)\

    def show_progres(self, variable: Literal["kcal", "protein", "carbs", "fats"]):
        return self.days[-1].print_progres_bar(variable)
