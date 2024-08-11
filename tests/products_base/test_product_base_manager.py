from pytest import fixture

from nutrition_app.products_base.products_base_manager import ProductsManager
from tests.mocked_connector import MockedConnector
from nutrition_app.models.product import Product


@fixture
def manager():
    manager = ProductsManager()
    manager.connector = MockedConnector()
    manager.connector.create_table(table_name="id_base", fields=("id", "name", "protein", "carbs", "fats", "kcal"))
    manager.add_product(Product("Ser", 0, 10, 10, 10, 120))
    return manager


class TestProductsManager:

    def test_create_table(self, manager):
        manager.connector.create_table("test", (1, 2, 3))
        table = manager.connector.get_table("test")

        assert table == {1: [], 2: [], 3: []}

    def test_get_id(self, manager):
        id_ = manager.get_id()

        assert id_ == 1

    def test_add_product(self, manager):
        table = manager.connector.get_table("id_base")
        assert "Ser" in table["name"]

    def test_get_product_by_id(self, manager):
        product = manager.get_product_by_id(0)

        assert product == Product("Ser", 0, 10, 10, 10, 120)

    def test_get_product_by_name(self, manager):
        product = manager.get_product_by_name("ser")

        assert product == Product("Ser", 0, 10, 10, 10, 120)
