from nutrition_app.models.product import Product
from pytest import fixture
import pytest

@fixture
def product():
    product = Product(name= "ser", id = 99, protein=10, carbs=20, fats=20)
    return product

class TestProduct:
    @pytest.mark.parametrize("dose", (-6, 1000))
    def test_protein_wrong_dose(self, product, dose):
        with pytest.raises(expected_exception=ValueError):
            product.protein = dose
    @pytest.mark.parametrize("dose", (-5, 1005))
    def test_carbs_wrong_dose(self, product, dose):
        with pytest.raises(expected_exception=ValueError):
            product.carbs = 1000
    @pytest.mark.parametrize("dose", (-8, 1037))
    def test_fats_wrong_dose(self, product, dose):
        with pytest.raises(expected_exception=ValueError):
            product.fats = 1000
    def test_kcal_underdose(self, product):
        with pytest.raises(expected_exception=ValueError):
            product.kcal = -6

