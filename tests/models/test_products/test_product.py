from nutrition_app.models.product import Product
from pytest import fixture
import pytest
from nutrition_app import database_path
from pathlib import Path
import json


Product.PRODUCTS_DIR = Path(__file__).parent.parent.parent / "test_db" / "test_sql.db"


@fixture
def product():
    product = Product(name="ser", id_=10000, protein=10, carbs=20, fats=20)
    return product


class TestProduct:

    def test_repr(self, product):
        assert (
            f"{product.__class__.__name__}(name={product.name}, id={product.id_}, protein={product.protein}, carbs={product.carbs}, fats={product.fats}, kcal={product.kcal})"
            == product.__repr__()
        )

    def test_eq(self, product):
        product2 = Product(name="ser", id_=10000, protein=10, carbs=20, fats=20)
        assert product == product2

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

    def test_to_dict(self, product):
        assert product.to_dict() == product.to_dict()



