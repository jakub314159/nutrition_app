from typing import Literal

from nutrition_app.models.product import EatableProduct
from nutrition_app.user.user import User
from nutrition_app.work_flow.eating_day import Day


class DaysManager:
    """
    Class that manages days in the application.

    Attributes:
        days (list[Day]): list of Days.
        meal_order (None | list[str]): users meal order.
        user (User): the User needed to use the DayManager.
    """

    def __init__(self, user: User):
        self.days: list[Day] = []
        self.meal_order: None | list[str] = user.meal_order
        self.user = user

    def __repr__(self):
        return f"{self.__class__.__name__}(self.user={self.user})"

    def add_day(self) -> None:
        """
        Add a new day to self.days

        Returns:
            None
        """
        day = Day(user=self.user)
        self.days.append(day)

    def add_to_meal(self, index: int, products: list[EatableProduct]):
        """
        Add a product to a meal.

        Args:
            index(int): the meal order index.
            products (list[EatableProduct]): list of products added.

        Returns:
            None
        """
        for product in products:
            self.days[-1].meals[self.meal_order[index]].add_product(product)

    def show_progress(self, variable: Literal["kcal", "protein", "carbs", "fats"] | None = None) -> list[str | float]:
        """
        This shows user the progress from the day.

        Args:
            variable (Literal["kcal", "protein", "carbs", "fats"] | None): needed to get progress.

        Returns:
            list[str | float]: progress bar along with percentage and quantity of the item consumed.
        """
        return self.days[-1].get_progress_bar(variable)
