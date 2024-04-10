from nutrition_app.models.product import Product
from pytest import fixture
import pytest
from nutrition_app import products_dir
from pathlib import Path
import json


Product.PRODUCTS_DIR = Path(__file__).parent.parent.parent / "test_db"

@fixture
def product():
    product = Product(name="ser", id_=10000, protein=10, carbs=20, fats=20)
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

    def test_to_and_from_json_file(self, product):
        product.to_json_file()

        name = f"{product.id_}.json"
        path = product.PRODUCTS_DIR / name

        try:
            with open(path, "r") as file:
                inside = json.load(file)

            new_product = Product.from_json_file(product.id_)
        finally:
            path.unlink()



        assert product.name == inside["name"]
        assert product.id_ == inside["id_"]
        assert new_product == product

