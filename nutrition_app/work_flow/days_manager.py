import sqlite3
from pathlib import Path
from typing import Literal, Sequence

from nutrition_app.models.product import EatableProduct
from nutrition_app.sql_connector import SQLConnector
from nutrition_app.sql_connector.base_connector import BaseConnector
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.user.user import User
from nutrition_app.work_flow.eating_day import Day


class DaysConnector(SQLConnector):
    """
    Superclass of SQLConnector that appends it with one method.
    """

    def get_days(self, table_name: str, username_val, date_val) -> list[dict[str, int]]:
        """
        Method used to get a list of days displayed via dicts for a certain username and from a certain date.

        Args:
            table_name (str): name of the database table.
            username_val (str): username of the user.
            date_val (int): date from which all saved days will be returned.

        Returns:
            list[dict[str, int]]: list of days represented by dicts.
        """
        connection = sqlite3.connect(str(self._database_path))
        cursor = connection.cursor()

        query = f"SELECT * FROM {table_name} WHERE username = '{username_val}' AND date >= {date_val}"

        res = cursor.execute(query)
        many = res.fetchall()
        keys = [desc[0] for desc in res.description]
        result_list = []

        for record in many:
            result_list.append({k: v for k, v in zip(keys, record)})
        connection.close()

        return result_list


class DaysManager:
    """
    Class that manages days in the application.

    Attributes:
        days (list[Day]): list of Days.
        meal_order (None | list[str]): users meal order.
        user (User): the User needed to use the DayManager.
    """

    def __init__(self, username: str, user: User, connector: BaseConnector | None = None):
        self.days: list[Day] = []
        self.meal_order: None | list[str] = user.meal_order
        self.user = user
        self.username = username
        self.connector = connector or DaysConnector(database_path=Path(__file__).parents[1] / "days_database.db")
        self.name = "days"
        self._create_table(
            self.name,
            (
                "id",
                "username",
                "date",
                "kcal_eaten",
                "protein_eaten",
                "carbs_eaten",
                "fats_eaten",
                "kcal_target",
                "protein_target",
                "carbs_target",
                "fats_target",
            ),
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(self.user={self.user})"

    def _create_table(self, table_name: str, fields: Sequence[str]) -> None:
        """
        Creates a products table if the table doesn't exist.

        Args:
            table_name(str): the name of the table.
            fields(Sequence[str]): the fields in the table.

        Returns:
            None
        """
        self.connector.create_table(table_name, fields)

    def add_day(self, date: int) -> None:
        """
        Add a day to self.days

        Args:
            date(int): date of the day.

        Returns:
            None
        """
        day = Day(user=self.user, date=date)
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

    def get_progress(self, variable: Literal["kcal", "protein", "carbs", "fats"] | None = None) -> list[str | float]:
        """
        Get progress bar containing the amount of micronutrient consumed, users target and the progress percentage.

        Args:
            variable (Literal["kcal", "protein", "carbs", "fats"] | None): needed to get progress.

        Returns:
            list[str | float]: progress bar along with percentage and quantity of the item consumed.
        """
        return self.days[-1].get_progress_bar(variable)

    def get_meal_progress(self, meal_name):
        return self.days[-1].get_meal_progress(meal_name)

    def save_to_database(self, date: int | None = None) -> None:
        """
        Save a Day to database.

        Args:
            date(int): the representation of the date yy:mm:dd

        Returns:
            None
        """
        date = date or self.days[-1].date
        _id = hash(str(self.username) + str(date))
        day = [x for x in self.days if x.date == date][0]
        day_info = day.to_tuple()
        self.connector.add_to_table(self.name, [(_id, self.username, date, *day_info)])

    def from_database(self, start_date: int) -> list[Day]:
        """
        Get a list of Days from database.

        Args:
            start_date(int): the representation of the date yy:mm:dd from which the days start.

        Returns:
            list[Day]: list of day objects.
        """
        records = self.connector.get_days(self.name, self.username, start_date)

        days = []

        for item in records:
            days.append(
                Day(
                    date=item["date"],
                    daily_target=DailyTarget(
                        kcal=item["kcal_target"],
                        protein=item["protein_target"],
                        carbs=item["carbs_target"],
                        fats=item["fats_target"],
                    ),
                    meal_order=["breakfast", "dinner", "snack", "supper"],
                    progress={
                        "kcal": item["kcal_eaten"],
                        "protein": item["protein_eaten"],
                        "carbs": item["carbs_eaten"],
                        "fats": item["fats_eaten"],
                    },
                )
            )

        return days
