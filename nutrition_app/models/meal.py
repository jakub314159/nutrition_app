from nutrition_app.models.product import BaseProduct


class Meal:
    def __init__(self, products: dict[BaseProduct:int, ...]):
        self.products = products
