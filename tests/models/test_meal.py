import pytest
from pytest import fixture
from nutrition_app.models.meal import Meal
from nutrition_app.models.product import Product, EatableProduct
from nutrition_app.models.fast_product import FastProduct


@fixture
def meal():
    product1 = EatableProduct(mass=100, product=Product(name="ser", id_=54374, protein=10, carbs=20, fats=20))
    product2 = FastProduct(name="ser", kcal=100.9, protein=10, carbs=20, fats=20)
    meal = Meal(products=[product1, product2])
    return meal


class TestMeal:
    def test_repr(self, meal):
        assert (
            meal.__repr__()
            == "Meal(product=[EatableProduct(mass=100, product=Product(name=ser, id_=54374, protein=10, carbs=20, fats=20, kcal=300)), FastProduct(name=ser, kcal=100.9, protein=10, carbs=20, fats=20)])"
        )

    def test_add_product(self, meal):
        product3 = EatableProduct(
            mass=10,
            product=Product(name="ser", id_=246547, protein=10, carbs=20, fats=20),
        )

        meal.add_product(product3)
        assert len(meal.products) == 3

    def test_delete_product_value_error(self, meal):
        with pytest.raises(expected_exception=ValueError):
            meal.delete_product(len(meal.products) + 1)

    def test_delete_product(self, meal):
        meal.delete_product(1)
        assert len(meal.products) == 1

    def test_count_ov_mass(self, meal):
        ov_mass = sum([x.mass for x in meal.products if isinstance(x, EatableProduct)])

        assert ov_mass == meal.count_ov_mass()

    def test_count_ov_kcal(self, meal):
        ov_kcal = sum([x.kcal for x in meal.products])

        assert ov_kcal == meal.count_ov_kcal()

    def test_count_ov_protein(self, meal):
        ov_protein = sum([x.protein for x in meal.products])

        assert ov_protein == meal.count_ov_protein()

    def test_count_ov_carbs(self, meal):
        ov_carbs = sum([x.carbs for x in meal.products])

        assert ov_carbs == meal.count_ov_carbs()

    def test_count_ov_fats(self, meal):
        ov_fats = sum([x.fats for x in meal.products])

        assert ov_fats == meal.count_ov_fats()

    def test_to_dict(self, meal):
        assert meal.to_dict() == meal.__dict__
