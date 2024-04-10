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

    def test_to_protein(self, eatable):
        assert eatable.to_protein() == 10

    def test_to_carbs(self,eatable):
        assert eatable.to_carbs() == 20

    def test_to_fats(self,eatable):
        assert eatable.to_fats() == 30

    def test_to_kcal(self, eatable):
        assert eatable.to_kcal() == eatable.product.protein * 4 + eatable.product.carbs * 4 + eatable.product.fats * 9

   
