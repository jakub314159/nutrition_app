from nutrition_app.numerical_attribute import NumericalAttribute


class FastProduct:
    """
    This class makes an object similar to the Product, but this one has less arguments so that it could be made easily.

    Attributes:
      name: This is the name of the product
      kcal: This is the number of calories that the product has
      protein: This is the number of proteins that the product has
      carbs: This is the number of carbs that the product has
      fats: This is the number of fats that the product has
    """

    kcal = NumericalAttribute()
    protein = NumericalAttribute()
    carbs = NumericalAttribute()
    fats = NumericalAttribute()

    def __init__(
        self, name: str, kcal: float, protein: float, carbs: float, fats: float
    ):
        self.name = name
        self.kcal = kcal
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
