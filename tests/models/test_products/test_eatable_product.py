import pytest

from nutrition_app.models.product import *
from pytest import fixture


@fixture
def eatable():
    product = Product(name="cheese", id_=99, protein=10, carbs=20, fats=30)
    eatable = EatableProduct(mass=100, product=product)
    return eatable


class TestEatableProduct:

    def test_mass_underdose(self, eatable):
        with pytest.raises(expected_exception=ValueError):
            eatable.mass = -100
