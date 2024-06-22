import pytest

from nutrition_app.user.user import User
from pytest import fixture


@fixture
def user():
    user = User(name="Jan", surname="Kowalski", weight=70, height=170, age=18, gender="male")
    return user


class TestUser:

    def test_repr(self, user):
        assert (
            f"{user.__class__.__name__}(name={user.name}, surname={user.surname}, weight={user.weight}, height={user.height}, age={user.age}, gender={user.gender}, daily_target={user.daily_target}, meal_order={user.meal_order})"
            == user.__repr__()
        )

    def test_eq_true(self, user):
        user2 = User(name="Jan", surname="Kowalski", weight=70, height=170, age=18, gender="male")
        assert user == user2

    def test_eq_false(self, user):
        user2 = User(
            name="John",
            surname="Majewski",
            weight=70,
            height=170,
            age=18,
            gender="male",
        )
        assert user != user2

    def test_age_below_0(self, user):
        with pytest.raises(expected_exception=ValueError):
            user.age = -10

    def test_height_below_0(self, user):
        with pytest.raises(expected_exception=ValueError):
            user.height = -10

    def test_weight_below_0(self, user):
        with pytest.raises(expected_exception=ValueError):
            user.weight = -10

    def test_count_bmi(self, user):
        assert user.count_bmi() == 24.22

    def test_create_daily_target(self, user):
        user.create_daily_target(kcal=170, protein=10, carbs=10, fats=10)
        assert (
            user.daily_target.kcal == 170
            and user.daily_target.protein == 10
            and user.daily_target.carbs == 10
            and user.daily_target.fats == 10
        )

    def test_set_daily_target(self, user):
        user.set_daily_target(activity=3)
        assert user.daily_target.kcal == 2700

    def test_set_meal_order(self, user):
        user.set_meal_order(["1", "2", "3"])
        assert user.meal_order == ["1", "2", "3"]

    def test_from_dict(self, user):
        data = user.to_dict()
        new = User.from_dict(data)

        assert new == user
