from pathlib import Path
from pytest import fixture
import pytest

from nutrition_app.models.product import *



Product.PRODUCTS_DIR = Path(__file__).parent.parent.parent / "test_db" / "test_sql.db"


@fixture
def product():
    product = Product(name="ser", id_=10000, protein=10, carbs=20, fats=20)
    return product


class TestProduct:
    def test_repr(self, product):
        assert product.__repr__() == 'Product(name=ser, id_=10000, protein=10, carbs=20, fats=20, kcal=300)'

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


@fixture
def eatable():
    product = Product(name="cheese", id_=99, protein=10, carbs=20, fats=30)
    eatable = EatableProduct(mass=1000, product=product)
    return eatable


class TestEatableProduct:
    def test_repr(self, eatable):
        assert eatable.__repr__() == 'EatableProduct(mass=1000, product=Product(name=cheese, id_=99, protein=10, carbs=20, fats=30, kcal=390))'

    def test_mass_underdose(self, eatable):
        with pytest.raises(expected_exception=ValueError):
            eatable.mass = -100

    def test_protein(self, eatable):
        assert eatable.protein == 100

    def test_carbs(self, eatable):
        assert eatable.carbs == 200

    def test_fats(self, eatable):
        assert eatable.fats == 300
