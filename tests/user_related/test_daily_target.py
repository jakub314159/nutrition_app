import pytest
from pytest import fixture
from nutrition_app.user_related.daily_target import DailyTarget, IncorrectMacroError


@fixture
def daily_target():
    daily_target = DailyTarget()
    return daily_target


class TestDailyTarget:

    def test_create_daily_target(self, daily_target):
        with pytest.raises(expected_exception=IncorrectMacroError) as e:
            daily_target.create_daily_target(kcal=10, protein=100, carbs=100, fats=100)
        assert e.match(
            "kcal from protein, carbs and fats is not adding to the amount of kcal."
        )

    def test_set_daily_target(self, daily_target):
        daily_target.set_daily_target(
            weight=70, height=170, activity=3, age=18, gender="male"
        )
        assert daily_target.kcal == 2700
