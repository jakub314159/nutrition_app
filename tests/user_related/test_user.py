import pytest

from nutrition_app.user_related.user import User
from  pytest import fixture

@fixture
def user():
    user = User(name="Jan", surname="Kowalski", weight=70, height= 170, age= 18, gender="male")
    return user

class TestUser:
    def test_age_below_0(self, user):
        with pytest.raises(expected_exception= ValueError):
            user.age = -10

    def test_height_below_0(self, user):
        with pytest.raises(expected_exception= ValueError):
            user.height = -10

    def test_weight_below_0(self, user):
        with pytest.raises(expected_exception= ValueError):
            user.weight = -10

    def test_count_bmi(self, user):
        assert user.count_bmi() == 24.22

    def test_set_daily_target(self, user):
        user.set_daily_target(activity= 3)
        assert user.daily_target.kcal == 2700