from nutrition_app.models.product import Product
from pytest import fixture
import pytest


@fixture
def base_product():
    base_product = Product(name="ser", id_=99, protein=10, carbs=20, fats=20)
    return base_product


class TestBaseProduct:
    @pytest.mark.parametrize("dose", (-6, 1000))
    def test_protein_wrong_dose(self, base_product, dose):
        with pytest.raises(expected_exception=ValueError):
            base_product.protein = dose

    @pytest.mark.parametrize("dose", (-5, 1005))
    def test_carbs_wrong_dose(self, base_product, dose):
        with pytest.raises(expected_exception=ValueError):
            base_product.carbs = 1000

    @pytest.mark.parametrize("dose", (-8, 1037))
    def test_fats_wrong_dose(self, base_product, dose):
        with pytest.raises(expected_exception=ValueError):
            base_product.fats = 1000

    def test_kcal_underdose(self, base_product):
        with pytest.raises(expected_exception=ValueError):
            base_product.kcal = -6
