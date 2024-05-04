from pytest import fixture
from nutrition_app.user_related.daily_target import DailyTarget

@fixture
def daily_target():
    daily_target = DailyTarget()
    return daily_target

class TestDailyTarget:
    def test_set_daily_target(self, daily_target):
        daily_target.set_daily_target(weight=70, height= 170, activity= 3, age= 18, gender= "male")
        assert daily_target.kcal == 2700
