from nutrition_app.models.product import EatableProduct
from nutrition_app.models.fast_product import FastProduct
from nutrition_app.error_station import error_base


class Meal:
    """
    Meal is a class, that hold a list o products (class EatableProduct or FastProduct) and it's variables (for example: name, protein, carbs, fats and kcal).

    Attributes:
        products(list[EatableProduct | FastProduct] | None): list that holds items from class EatableProduct, FastProduct or an empty list if products are not provided.
    """

    def __init__(self, products: list[EatableProduct | FastProduct] | None = None):
        self.products = products or []

    def __repr__(self):
        return f"{self.__class__.__name__}(product={self.products})"

    def add_product(self, product: EatableProduct | FastProduct) -> None:
        """
        Add a product to self.products

        Args:
            product(EatableProduct | FastProduct): an EatableProduct object or a FastProduct object that will be added to self.products

        Returns:
            None
        """
        self.products.append(product)

    def delete_product(self, index: int) -> None:
        """
        Deletes a product from the product list.

        Args:
            index(int): index to delete a particular item from self.products

        Raises:
            ValueError: if the index value is to high.

        Returns:
            None
        """
        if index >= len(self.products):
            raise ValueError(error_base.get("E10").format(len(self.products) - 1))

        self.products.pop(index)

    def count_ov_mass(self) -> float | str:
        """
        Count overall mass of the objects class EatableProduct in self.products

        Returns:
            float | str: Returns all the mass from Eatable products inside list self.products or a 0 if products are class FastProduct or not given.
        """

        ov_mass = sum([x.mass for x in self.products if isinstance(x, EatableProduct)])
        return ov_mass

    def count_ov_kcal(self) -> float:
        """
        Count overall calories of the meal.

        Returns:
            float: total calories in the meal.
        """
        ov_kcal = sum([x.kcal for x in self.products])
        return ov_kcal

    def count_ov_protein(self) -> float:
        """
        Count overall protein of the meal.

        Returns:
            float: total protein in the meal.
        """
        ov_protein = sum([x.protein for x in self.products])
        return ov_protein

    def count_ov_carbs(self) -> float:
        """
        Count overall carbohydrates of the meal.

        Returns:
            float: total carbs in the meal.
        """
        ov_carbs = sum([x.carbs for x in self.products])
        return ov_carbs

    def count_ov_fats(self) -> float:
        """
        Counts overall fats of the meal.

        Returns:
            float: total fats in the meal
        """
        ov_fats = sum([x.fats for x in self.products])
        return ov_fats

    def to_dict(self) -> dict[str]:
        """
        This makes all meal arguments to dict.

        Returns:
            dict[str]: the meal dict.
        """
        return self.__dict__
