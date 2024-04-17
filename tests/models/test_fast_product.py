from nutrition_app.models.fast_product import FastProduct
from pytest import fixture


@fixture
def fast_product():
    fast_product = FastProduct("cheese", 100.5, 23, 10, 20)

    return fast_product


class TestFastProduct:
    pass
