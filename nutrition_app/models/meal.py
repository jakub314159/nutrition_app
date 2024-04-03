from nutrition_app.models.product import Product


class Meal:
    def __init__(self, products: list[Product] | None = None):
        self.products = products or []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def delete_product(self, index: int) -> None:
        self.products.pop(index)

    def count_ov_mass(self) -> float:
        ov_mass = sum([x.mass for x in self.products])
        return ov_mass

    def count_ov_kcal(self) -> float:
        ov_kcal = sum([x.kcal for x in self.products])
        return ov_kcal

    def count_ov_protein(self) -> float:
        ov_protein = sum([x.protein for x in self.products])
        return ov_protein

    def count_ov_carbs(self) -> float:
        ov_carbs = sum([x.carbs for x in self.products])
        return ov_carbs

    def count_ov_fats(self) -> float:
        ov_fats = sum([x.fats for x in self.products])
        return ov_fats

if __name__ == "__main__":
    product1 = Product(mass=100,name="cheese",id_=10923,protein=10,carbs=10,fats=10)
    product2 = Product(mass=345,name="potato",id_=1353,protein=10,carbs=10,fats=10)
    new_meal = Meal(products=[product1, product2])

    print(new_meal.count_ov_fats())
    print(new_meal.count_ov_kcal())




