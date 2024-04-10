from nutrition_app.models.product import EatableProduct, Product


class Meal:
    """
    Meal is a class, that hold a list o products (class Product) and it's variables.

    Args:
        products: a list thet holds items from class Product or an empty list if Products are not given.
    """

    def __init__(self, products: list[EatableProduct] | None = None):
        self.products = products or []

    def add_product(self, product: EatableProduct) -> None:
        """This adds a product to the product list."""
        self.products.append(product)

    def delete_product(self, index: int) -> None:
        """This deletes a product from the product list."""
        self.products.pop(index)

    def count_ov_mass(self) -> float:
        """This counts overall mass of the meal."""
        ov_mass = sum([x.mass for x in self.products])
        return ov_mass

    def count_ov_kcal(self) -> float:
        """This counts overall calories of the meal."""
        ov_kcal = sum([x.product.kcal for x in self.products])
        return ov_kcal

    def count_ov_protein(self) -> float:
        """This counts overall protein of the meal."""
        ov_protein = sum([x.product.protein for x in self.products])
        return ov_protein

    def count_ov_carbs(self) -> float:
        """This counts overall carbohydrates of the meal."""
        ov_carbs = sum([x.product.carbs for x in self.products])
        return ov_carbs

    def count_ov_fats(self) -> float:
        """This counts overall fats of the meal."""
        ov_fats = sum([x.product.fats for x in self.products])
        return ov_fats


if __name__ == "__main__":
    product1 = EatableProduct(
        mass=100,
        product=Product(name="cheese", id_=10923, protein=10, carbs=10, fats=10),
    )
    product2 = EatableProduct(
        mass=345,
        product=Product(name="potato", id_=1353, protein=10, carbs=10, fats=10),
    )
    new_meal = Meal(products=[product1, product2])

    print(new_meal.count_ov_fats())
    print(new_meal.count_ov_kcal())
