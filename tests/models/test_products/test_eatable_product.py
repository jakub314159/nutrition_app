import pytest

from nutrition_app.models.product import *
from pytest import fixture


@fixture
def eatable():
    product = Product(name="cheese", id_=99, protein=10, carbs=20, fats=30)
    eatable = EatableProduct(mass=1000, product=product)
    return eatable


class TestEatableProduct:

    def test_mass_underdose(self, eatable):
        with pytest.raises(expected_exception=ValueError):
            eatable.mass = -100

    def test_protein(self, eatable):
        assert eatable.protein == 100

    def test_carbs(self, eatable):
        assert eatable.carbs == 200

    def test_fats(self, eatable):
        assert eatable.fats == 300
