import pytest
from pytest import fixture
from nutrition_app.user_related.daily_target import DailyTarget, IncorrectMacroError


@fixture
def daily_target():
    daily_target = DailyTarget()
    return daily_target


class TestDailyTarget:

    def test_repr(self, daily_target):
        assert (
            f"{daily_target.__class__.__name__}(kcal={daily_target.kcal}, protein={daily_target.protein}, carbs={daily_target.carbs}, fats={daily_target.fats})"
            == daily_target.__repr__()
        )

    def test_create_daily_target_incorrect_macro_error(self, daily_target):
        with pytest.raises(expected_exception=IncorrectMacroError) as e:
            daily_target.create_daily_target(kcal=10, protein=100, carbs=100, fats=100)
        assert e.match(
            "kcal from protein, carbs and fats is not adding to the amount of kcal."
        )

    def test_create_daily_target(self, daily_target):
        daily_target.create_daily_target(kcal=170, protein=10, carbs=10, fats=10)
        assert (
            daily_target.kcal == 170
            and daily_target.protein == 10
            and daily_target.carbs == 10
            and daily_target.fats == 10
        )

    def test_set_daily_target_activity_error(self, daily_target):
        with pytest.raises(expected_exception=ValueError):
            daily_target.set_daily_target(
                weight=70, height=170, activity=6, age=18, gender="male"
            )

    def test_set_daily_target_male(self, daily_target):
        daily_target.set_daily_target(
            weight=70, height=170, activity=3, age=18, gender="male"
        )
        assert daily_target.kcal == 2700

    def test_set_daily_target_female(self, daily_target):
        daily_target.set_daily_target(
            weight=70, height=170, activity=3, age=18, gender="female"
        )
        assert daily_target.kcal == 2390

    def test_set_daily_target_gender_error(self, daily_target):
        with pytest.raises(expected_exception=ValueError):
            daily_target.set_daily_target(
                weight=70, height=170, activity=3, age=18, gender="gender"
            )
