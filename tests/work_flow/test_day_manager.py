from pytest import fixture


from nutrition_app.models.product import EatableProduct
from nutrition_app.models.product import Product
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.user.user import User
from nutrition_app.work_flow.days_manager import DaysManager
from nutrition_app.work_flow.eating_day import Day
from tests.mocked_connector import MockedConnector


@fixture
def manager():
    manager = DaysManager(
        username="test",
        user=User("test", "test", 18, 1.8, 75, "male", DailyTarget(protein=100, carbs=100, fats=100, kcal=1700)),
        connector=MockedConnector(),
    )

    return manager


class TestDayManager:
    def test_repr(self, manager):
        assert manager.__repr__() == (
            "DaysManager(self.user=User(name=test, surname=test, weight=75, height=180.0, "
            "age=18, gender=male, daily_target=DailyTarget(kcal=1700, protein=100, "
            "carbs=100, fats=100), meal_order=['breakfast', 'dinner', 'snack', "
            "'supper']))"
        )

    def test_add_day(self, manager):
        manager.add_day(240101)
        assert len(manager.days) == 1

    def test_add_to_meal(self, manager):
        manager.add_day(240101)
        manager.add_to_meal(0, [EatableProduct(product=Product("ser", 0, 10, 10, 10, 120), mass=100)])
        assert manager.days[0].meals[manager.user.meal_order[0]].products[0].product == Product(
            "ser", 0, 10, 10, 10, 120
        )

    def test_show_progress(self, manager):
        manager.add_day(240101)
        manager.add_to_meal(0, [EatableProduct(product=Product("ser", 0, 10, 10, 10, 120), mass=100)])
        eaten = manager.show_progress("kcal")

        assert eaten[1] == 120

    def test_save_to_database(self, manager):
        manager.add_day(240101)
        manager.add_to_meal(0, [EatableProduct(product=Product("ser", 0, 10, 10, 10, 120), mass=100)])
        manager.save_to_database()

        record = manager.connector.get_record_from_table(
            manager.name, "id", hash(str(manager.username) + str(manager.days[-1].date))
        )

        assert record["id"] == hash(str(manager.username) + str(manager.days[-1].date))

    def test_from_database(self, manager):
        manager.days = [
            Day(user=manager.user, date=240101),
            Day(user=manager.user, date=240102),
            Day(user=manager.user, date=240103),
        ]
        manager.save_to_database(240101)
        manager.save_to_database(240102)
        manager.save_to_database(240103)
        days_list = manager.from_database(240101)

        expected = [
            Day(
                user=None,
                date=240101,
                daily_target=DailyTarget(kcal=1700, protein=100, carbs=100, fats=100),
                meal_order=["breakfast", "dinner", "snack", "supper"],
                progress={"kcal": 0, "protein": 0, "carbs": 0, "fats": 0},
            ),
            Day(
                user=None,
                date=240102,
                daily_target=DailyTarget(kcal=1700, protein=100, carbs=100, fats=100),
                meal_order=["breakfast", "dinner", "snack", "supper"],
                progress={"kcal": 0, "protein": 0, "carbs": 0, "fats": 0},
            ),
            Day(
                user=None,
                date=240103,
                daily_target=DailyTarget(kcal=1700, protein=100, carbs=100, fats=100),
                meal_order=["breakfast", "dinner", "snack", "supper"],
                progress={"kcal": 0, "protein": 0, "carbs": 0, "fats": 0},
            ),
        ]

        assert days_list == expected
