from typing import Sequence

from nutrition_app.models.product import Product
from nutrition_app.sql_connector.sql_connector import SQLConnector
from pathlib import Path


class ProductsManager:
    def __init__(self):
        self.connector = SQLConnector(database_path=Path(__file__).parent / "products_id_base.db")
        self.name = "id_base"
        self._create_table(table_name=self.name, fields=("id", "name", "protein", "carbs", "fats", "kcal"))

    def _create_table(self, table_name: str, fields: Sequence[str]):
        """
        This creates a products table.
        """
        self.connector.create_table(table_name, fields)

    def get_id(self):
        """
        Returns:
            This returns the new largest id for another product.
        """
        table = self.connector.get_table(self.name)

        if table["id"] == []:
            new_id = 0
        else:
            new_id = max(table["id"]) + 1

        return new_id

    def add_product(self, product: "Product"):
        """
        Args:
            product: The product that is going to be added to the sql database.
        """
        id_ = self.get_id()
        self.connector.add_to_table(
            self.name, [(id_, product.name, product.protein, product.carbs, product.fats, product.kcal)]
        )

    def get_product_by_id(self, id_: int) -> "Product":
        """
        This lets user get a product by id from sql database.
        Args:
            id_: id needed to search db.

        Returns:
            Object from class Product.
        """
        product = self.connector.get_record_from_table(self.name, "id", id_)
        return Product(product["name"], id_, product["protein"], product["carbs"], product["fats"], product["kcal"])

    def get_product_by_name(self, name: str) -> "Product":
        """
        This lets user get a product by name from sql database.
        Args:
            name: name needed to search db.

        Returns:
            Object from class Product.
        """
        product = self.connector.get_record_from_table(self.name, "name", name)
        return Product(product["name"], product["protein"], product["carbs"], product["fats"], product["kcal"])
