from nutrition_app.models.product import Product
from pytest import fixture
import pytest
from nutrition_app import products_dir
from pathlib import Path
import json


Product.PRODUCTS_DIR = Path(__file__).parent.parent.parent / "test_db"
Product.PRODUCTS_DIR.mkdir(exist_ok=True)


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

    def test_to_json_file_file_exists_error(self, product):
        with pytest.raises(expected_exception=FileExistsError):
            product.id_ = 10
            product.to_json_file()

    def test_from_json_file_file_not_found(self, product):
        with pytest.raises(expected_exception=FileNotFoundError):
            product.from_json_file(id_=124681234)

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
