from nutrition_app.models.fast_product import FastProduct
from pytest import fixture


@fixture
def fast_product():
    fast_product = FastProduct("cheese", 100.5, 23, 10, 20)

    return fast_product


class TestFastProduct:
    def test_repr(self, fast_product):
        assert fast_product.__repr__() == "FastProduct(name=cheese, kcal=100.5, protein=23, carbs=10, fats=20)"
