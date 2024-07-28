from pytest import fixture


from nutrition_app.models.product import EatableProduct
from nutrition_app.models.product import Product
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.user.user import User
from nutrition_app.work_flow.day_manager import DaysManager

@fixture
def manager():
    manager = DaysManager(user= User("test", "test", 18, 1.8, 75, "male", DailyTarget(protein= 100, carbs= 100, fats= 100, kcal= 1700)))
    return  manager

class TestDayManager:
    def test_repr(self, manager):
        assert manager.__repr__() == ('DaysManager(self.user=User(name=test, surname=test, weight=75, height=180.0, '
 'age=18, gender=male, daily_target=DailyTarget(kcal=1700, protein=100, '
 "carbs=100, fats=100), meal_order=['breakfast', 'dinner', 'snack', "
 "'supper']))")

    def test_add_day(self, manager):
        manager.add_day()
        assert len(manager.days) == 1

    def test_add_to_meal(self, manager):
        manager.add_day()
        manager.add_to_meal(0, [EatableProduct(product=Product("ser", 0, 10, 10, 10, 120), mass= 100)])
        assert manager.days[0].meals[manager.user.meal_order[0]].products[0].product == Product("ser", 0, 10, 10, 10, 120)

    def test_show_progress(self, manager):
        manager.add_day()
        manager.add_to_meal(0, [EatableProduct(product=Product("ser", 0, 10, 10, 10, 120), mass= 100)])
        eaten = manager.show_progress("kcal")

        assert eaten[1] == 120



