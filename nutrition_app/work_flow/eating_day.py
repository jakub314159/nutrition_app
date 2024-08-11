from typing import Literal, Sequence
from datetime import datetime
from typing import TypedDict

from nutrition_app.models.fast_product import FastProduct
from nutrition_app.models.meal import Meal
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.user.user import User
from nutrition_app.models.product import EatableProduct
from nutrition_app.error_station import error_base


class ProgressDict(TypedDict):
    percentage: float
    actual: float
    target: float


class Day:
    """
    This class supports a single day of eating for the user.

    Attributes:
        user (User): an object of the User class.
        meals (dict[str, Meal]): meals in the day.
        progress (dict[str: int]): the progress from the day.
        date (int): the date when the eating plan is created.
    """

    def __init__(
        self,
        user: User | None = None,
        date: int | None = None,
        daily_target: DailyTarget | None = None,
        meal_order: None = None,
        progress: dict[str, int] | None = None,
    ):
        self.user = user or None
        self.daily_target = daily_target if user is None else user.daily_target
        self.meal_order = meal_order if user is None else user.meal_order
        self.meals: dict[str, Meal] = {meal_name: Meal() for meal_name in self.meal_order}
        self.progress: dict[str, int] = progress or {"kcal": 0, "protein": 0, "carbs": 0, "fats": 0}
        self.date = date or self.set_date()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(user={self.user}, date={self.date}, daily_target={self.daily_target}, meal_order={self.meal_order}, progress={self.progress})"

    def __eq__(self, other: "Day") -> bool:
        if self.date == other.date and self.user == other.user:
            return True
        return False

    @staticmethod
    def set_date() -> int:
        """
        Get date of the Day.

        Returns:
            int: the yy:mm:dd representation of the date.
        """
        now = datetime.now()
        return now.strftime("%y%m%d")

    def _validate(self, meal_index: int) -> None:
        """
        Check if meal_index is in range of the users meal order.

        Args:
            meal_index(int): index that is going to be checked.

        Raises:
            ValueError: if the index is to high.

        Returns:
            None
        """
        if meal_index >= len(self.meal_order):
            raise ValueError(error_base.get("E10").format(len(self.meal_order) - 1))

    def add_products_to_meal(self, meal_index: int, products: Sequence[EatableProduct | FastProduct]) -> None:
        """
        This lets the user add a list of EatableProducts and / or FastProducts.

        Args:
            meal_index(int): index that specifies the meal to which the products will be added.
            products (Sequence[EatableProduct | FastProduct]): list of objects from EatableProduct or FastProduct classes.

        Returns:
            None
        """
        self._validate(meal_index=meal_index)
        for product in products:
            self.meals[self.meal_order[meal_index]].add_product(product)

    def delete_product_from_meal(self, meal_index: int, product_index: int) -> None:
        """
        Delete a product from the meal.

        Args:
            meal_index(int): This is the index that specifies the meal to which the products will be added.
            product_index(int): This is the index that specifies the product from which the products will be deleted.

        Returns:
            None
        """
        self._validate(meal_index=meal_index)
        self.meals[self.meal_order[meal_index]].delete_product(product_index)

    @property
    def kcal_progress(self) -> ProgressDict:
        actual = sum([x.count_ov_kcal() for x in self.meals.values()])

        self.progress["kcal"] = round(actual / self.daily_target.kcal * 100)

        return {
            "percentage": self.progress["kcal"],
            "actual": round(actual, 1),
            "target": round(self.daily_target.kcal, 1),
        }

    @property
    def protein_progress(self) -> ProgressDict:
        actual = sum([x.count_ov_protein() for x in self.meals.values()])

        self.progress["protein"] = round(actual / self.daily_target.protein * 100)

        return {
            "percentage": self.progress["protein"],
            "actual": round(actual, 1),
            "target": round(self.daily_target.protein, 1),
        }

    @property
    def carbs_progress(self) -> ProgressDict:
        actual = sum([x.count_ov_carbs() for x in self.meals.values()])

        self.progress["carbs"] = round(actual / self.daily_target.carbs * 100)

        return {
            "percentage": self.progress["carbs"],
            "actual": round(actual, 1),
            "target": round(self.daily_target.carbs, 1),
        }

    @property
    def fats_progress(self) -> ProgressDict:
        actual = sum([x.count_ov_fats() for x in self.meals.values()])

        self.progress["fats"] = round(actual / self.daily_target.fats * 100)

        return {
            "percentage": self.progress["fats"],
            "actual": round(actual, 1),
            "target": round(self.daily_target.fats, 1),
        }

    def get_progress_bar(self, variable: Literal["kcal", "protein", "carbs", "fats"] | None = None) -> list[str, float]:
        """
        Get progress bar containing the amount of micronutrient consumed, users target and the progress percentage.

        Args:
            variable (Literal["kcal", "protein", "carbs", "fats"] | None): the nutrient on which the progres will be checked.

        Returns:
            list[str, float]: list containing the progres bar and the percentage.
        """
        match variable:
            case "kcal":
                local_progress = self.kcal_progress
            case "protein":
                local_progress = self.protein_progress
            case "carbs":
                local_progress = self.carbs_progress
            case "fats":
                local_progress = self.fats_progress
            case _:
                raise ValueError(error_base.get("E9").format(variable))

        full = round(local_progress["percentage"] / 5)

        if full >= 20:
            intake_info = f'overeaten_kcal: {local_progress["actual"] - local_progress["target"]}'
            if full == 20:
                intake_info = "progress: 100%"
            return [
                f"{variable}\t{20 * '▰'} {local_progress['actual']} / {local_progress['target']}, {intake_info}",
                local_progress["actual"],
            ]
        else:
            less = 20 - full
            return [
                f"{variable}\t{int(full) * '▰' + int(less) * '▱'} {local_progress['actual']} / {local_progress['target']}, progress: {local_progress['percentage']}%",
                local_progress["actual"],
            ]

    def to_tuple(self) -> tuple[float]:
        """
        Get a tuple containing consumed micronutrients and the days target.

        Returns:
            tuple[float]: all micronutrients eaten and the target.
        """
        return (
            self.kcal_progress["actual"],
            self.protein_progress["actual"],
            self.carbs_progress["actual"],
            self.fats_progress["actual"],
            self.daily_target.kcal,
            self.daily_target.protein,
            self.daily_target.carbs,
            self.daily_target.fats,
        )
