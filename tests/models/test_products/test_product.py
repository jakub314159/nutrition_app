import pytest

from nutrition_app.models.product import Product
from pytest import fixture

@fixture
def product():
    product = Product(mass= 100, name="cheese", id_ = 99, protein=10, carbs=20, fats=20)
    return product

class Test_product:

    def test_mass_underdose(self, product):
        with pytest.raises(expected_exception=ValueError):
            product.mass = -100