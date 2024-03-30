class Product:
    """
    this class creates a product

    arguments:
        name: the name of the product
        id: id of the product
        protein: the amount of protein in the product
        carbs: the amount of carbs in the product
        fats: the amount of fats in the product
        kcal: the amount of kilo-calories in the product
        kwargs:
            salt: the amount of salt in the product
            sugars: the amount of sugars in the product
            fiber: the amount of fiber in the product
    """

    def __init__(
        self,
        name: str,
        id: int,
        protein: float,
        carbs: float,
        fats: float,
        kcal: float | None = None,
        **kwargs,
    ):
        self.name = name
        self.id = id
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.kcal = kcal
        self.salt = kwargs.get("salt", None)
        self.sugars = kwargs.get("sugars", None)
        self.fiber = kwargs.get("fiber", None)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, id={self.id}, protein={self.protein}, carbs={self.carbs}, fats={self.fats}, kcal={self.kcal})"

    def __eq__(self, other: "Product"):
        return self.name == other.name and self.id == other.id

    @property
    def protein(self) -> float:
        return self._protein

    @protein.setter
    def protein(self, value) -> None:
        if value < 0 or value > 100:
            raise ValueError("Protein per 100g can be defined in range 0 - 100")
        self._protein = value

    @property
    def carbs(self) -> float:
        return self._carbs

    @carbs.setter
    def carbs(self, value) -> None:
        if value < 0 or value > 100:
            raise ValueError("Carbs per 100g can be defined in range 0 - 100")
        self._carbs = value

    @property
    def fats(self) -> float:
        return self._fats

    @fats.setter
    def fats(self, value) -> None:
        if value < 0 or value > 100:
            raise ValueError("Fats per 100g can be defined in range 0 - 100")
        self._fats = value

    @property
    def kcal(self) -> float:
        return self._kcal

    @kcal.setter
    def kcal(self, value) -> None:
        if value is None:
            value = self.protein * 4 + self.carbs * 4 + self.fats * 9
        if value <= 0:
            raise ValueError("kcal cannot be below or cannot be 0")

        self._kcal = value


if __name__ == "__main__":
    new_product = Product("ser", 1325243534, 100, 20, 25)
    sth = Product("ser", 1325243534, 10, 20, 25)
    print(new_product == sth)
