from typing import Literal
from datetime import datetime
from pathlib import Path
import json

from nutrition_app.user.daily_target import DailyTarget

from nutrition_app.models.fast_product import FastProduct
from nutrition_app.models.meal import Meal
from nutrition_app.user.user import User
from nutrition_app.models.product import EatableProduct, Product
from nutrition_app.error_station import error_base


class Day:
    """
    This class supports a single day of eating for the user.

    Attributes:
        user: an object of the User class.
        date: the date when the eating plan is created.
    """

    def __init__(self, user: User, date: str = None):
        self.user = user
        self.meals: dict[str, Meal] = {meal_name: Meal() for meal_name in self.user.meal_order}
        self.progres = {"kcal": 0, "protein": 0, "carbs": 0, "fats": 0}
        self.date = date or self.set_date()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(user={self.user})"

    def __eq__(self, other: "Day") -> bool:
        if self.date == other.date and self.user == other.user:
            return True
        return False

    @staticmethod
    def set_date():
        """
        This lets the user to set the date in wchih the user eats.
        Returns: str with calender date and the weekday.
        """
        now = datetime.now()
        week_dict = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturdey",
            6: "Sunday",
        }
        return f"{now.day}-{now.month}-{now.year}, {week_dict.get(now.weekday())}"

    def _validate(self, meal_index: int) -> None:
        """
        This checks if meal_index is in range of the users meal order.
        Args:
            meal_index: the index that is going to be checked.
        Raises:
            ValueError: an error from the error base satting that the index is to high.
        """
        if meal_index >= len(self.user.meal_order):
            raise ValueError(error_base.get("E10").format(len(self.user.meal_order) - 1))

    def add_to_meal(self, meal_index: int, products: list[EatableProduct | FastProduct]) -> None:
        """
        This lets the user add a list of EatableProducts and / or FastProducts.
        Args:
            meal_index: This is the index that specifies the meal to which the products will be added.
            products: the list of objects from EatableProduct or FastProduct classes.
        """
        self._validate(meal_index=meal_index)
        for product in products:
            self.meals[self.user.meal_order[meal_index]].add_product(product)

    def delete_from_meal(self, meal_index: int, product_index: int):
        """
        This lets the user to delete a product from the meal.
        Args:
            meal_index: This is the index that specifies the meal to which the products will be added.
            product_index: This is the index that specifies the product from which the products will be deleted.
        """
        self._validate(meal_index=meal_index)
        self.meals[self.user.meal_order[meal_index]].delete_product(product_index)

    @property
    def kcal_progres(self):
        self.progres["kcal"] = round(
            sum([x.count_ov_kcal() for x in self.meals.values()]) / self.user.daily_target.kcal * 100
        )
        return self.progres["kcal"]

    @property
    def protein_progres(self):
        self.progres["protein"] = round(
            sum([x.count_ov_protein() for x in self.meals.values()]) / self.user.daily_target.protein * 100
        )
        return self.progres["protein"]

    @property
    def carbs_progres(self):
        self.progres["carbs"] = round(
            sum([x.count_ov_carbs() for x in self.meals.values()]) / self.user.daily_target.carbs * 100
        )
        return self.progres["carbs"]

    @property
    def fats_progres(self):
        self.progres["fats"] = round(
            sum([x.count_ov_fats() for x in self.meals.values()]) / self.user.daily_target.fats * 100
        )
        return self.progres["fats"]

    def get_progres_bar(self, variable: Literal["kcal", "protein", "carbs", "fats"]) -> list[str]:
        """
        This lists progres for the user.
        Args:
            variable: the nutrient on which the progres will be checked,

        Returns:
            The list cointainig the progres bar and the procentage.
        """
        match variable:
            case "kcal":
                local_progress = self.kcal_progres
            case "protein":
                local_progress = self.protein_progres
            case "carbs":
                local_progress = self.carbs_progres
            case "fats":
                local_progress = self.fats_progres
            case _:
                raise ValueError(error_base.get("E9").format(variable))

        full = round(local_progress / 5)
        less = 20 - full
        return [int(full) * "▰" + int(less) * "▱", f"{self.progres[variable]}%"]
