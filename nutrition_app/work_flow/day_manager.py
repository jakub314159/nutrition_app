from typing import Literal

from nutrition_app.models.product import EatableProduct, Product
from nutrition_app.user.user import User
from nutrition_app.work_flow.eating_day import Day


class DaysManager:
    def __init__(self, user: User):
        self.days: list[Day] = []
        self.meal_order = user.meal_order
        self.user = user

    def __repr__(self):
        return f"{self.__class__.__name__}(self.user={self.user})"

    def add_day(self):
        """
        This lets user add a new day to self.days

        Returns: None
        """
        day = Day(user=self.user)
        self.days.append(day)

    def add_to_meal(self, index: int, products: list[EatableProduct]):
        """
        This lets user add a product to a meal.
        Args:
            index: the meal order index.
            products: list of products added.

        Returns: None
        """
        for product in products:
            self.days[-1].meals[self.meal_order[index]].add_product(product)

    def show_progress(self, variable: Literal["kcal", "protein", "carbs", "fats"] | None = None):
        """
        This shows user the progress from the day.
        Args:
            variable: needed to get progress.

        Returns:
            The progress bar along with percentage and quantity of the item consumed.
        """
        return self.days[-1].get_progress_bar(variable)
