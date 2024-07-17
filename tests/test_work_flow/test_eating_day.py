import json

from datetime import datetime
from pathlib import Path
from pytest import fixture, raises

from nutrition_app.models.product import EatableProduct, Product
from nutrition_app.work_flow.eating_day import Day
from nutrition_app.user.user import User
from nutrition_app.user.daily_target import DailyTarget


WEEK_DICT = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturdey",
    6: "Sunday",
}


@fixture
def day():
    target = DailyTarget()
    target.set_daily_target(weight=70, height=170, activity=3, age=18, gender="male")
    user = User(
        name="Jan",
        surname="Kowalski",
        weight=70,
        height=170,
        age=18,
        gender="male",
        daily_target=target,
    )
    day = Day(user=user)
    day.add_to_meal(
        meal_index=0,
        products=[
            EatableProduct(
                mass=100,
                product=Product(name="ser", id_=10000, protein=10, carbs=10, fats=10, kcal=170),
            )
        ],
    )
    return day


class TestDay:

    def test_repr(self, day):
        assert f"{day.__class__.__name__}(user={day.user})" == day.__repr__()

    def test_eq_true(self, day):
        target = DailyTarget()
        target.set_daily_target(weight=70, height=170, activity=3, age=18, gender="male")
        user = User(
            name="Jan",
            surname="Kowalski",
            weight=70,
            height=170,
            age=18,
            gender="male",
            daily_target=target,
        )
        day2 = Day(user=user)
        assert day == day2

    def test_eq_false(self, day):
        day2 = Day(
            user=User(
                name="John",
                surname="Lock",
                weight=70,
                height=170,
                age=18,
                gender="male",
            )
        )
        assert day != day2

    def test_set_date(self, day):
        now = datetime.now()

        assert day.set_date() == f"{now.day}-{now.month}-{now.year}, {WEEK_DICT.get(now.weekday())}"

    def test_validate(self, day):
        with raises(expected_exception=ValueError):
            day._validate(meal_index=len(day.user.meal_order) + 1)

    def test_add_to_meal(self, day):
        previous = len(day.meals["breakfast"].products)
        day.add_to_meal(
            meal_index=0,
            products=[
                EatableProduct(
                    mass=100,
                    product=Product(name="kurczak", id_=2345, protein=10, carbs=20, fats=20),
                )
            ],
        )

        assert len(day.meals["breakfast"].products) == previous + 1

    def test_delete_from_meal(self, day):
        previous = len(day.meals["breakfast"].products)
        day.delete_from_meal(0, 0)

        assert len(day.meals["breakfast"].products) == previous - 1

    def test_kcal_progres(self, day):
        assert day.kcal_progres == round(170 / day.user.daily_target.kcal * 100)

    def test_protein_progres(self, day):
        assert day.protein_progres == round(10 / day.user.daily_target.protein * 100)

    def test_carbs_progres(self, day):
        assert day.carbs_progres == round(10 / day.user.daily_target.carbs * 100)

    def test_fats_progres(self, day):
        assert day.fats_progres == round(10 / day.user.daily_target.fats * 100)

    def test_get_progres_bar_kcal_progres(self, day):
        day.kcal_progres
        full = round(day.progres["kcal"] / 5)
        less = 20 - full
        assert day.print_progres_bar(variable="kcal") == [
            int(full) * "▰" + int(less) * "▱",
            f"{day.progres['kcal']}%",
        ]

    def test_get_progres_bar_protein_progres(self, day):
        day.protein_progres
        full = round(day.progres["protein"] / 5)
        less = 20 - full
        assert day.print_progres_bar(variable="protein") == [
            int(full) * "▰" + int(less) * "▱",
            f"{day.progres['protein']}%",
        ]

    def test_get_progres_bar_carbs_progres(self, day):
        day.carbs_progres
        full = round(day.progres["carbs"] / 5)
        less = 20 - full
        assert day.print_progres_bar(variable="carbs") == [
            int(full) * "▰" + int(less) * "▱",
            f"{day.progres['carbs']}%",
        ]

    def test_get_progres_bar_fats_progres(self, day):
        day.fats_progres
        full = round(day.progres["fats"] / 5)
        less = 20 - full
        assert day.print_progres_bar(variable="fats") == [
            int(full) * "▰" + int(less) * "▱",
            f"{day.progres['fats']}%",
        ]

    def test_get_progres_bar_value_error(self, day):
        with raises(expected_exception=ValueError):
            day.print_progres_bar(variable="error")
