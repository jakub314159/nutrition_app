class BaseProduct:
    """
    This class creates a product blueprint

    Args:
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
        id_: int,
        protein: float,
        carbs: float,
        fats: float,
        kcal: float | None = None,
        **kwargs,
    ):
        self.name = name
        self.id_ = id_
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.kcal = kcal
        self.salt = kwargs.get("salt", None)
        self.sugars = kwargs.get("sugars", None)
        self.fiber = kwargs.get("fiber", None)

    def __repr__(self) -> str:
        """
        This is the representation of the class when the command print is run on one of the objects from this class.
        """
        return f"{self.__class__.__name__}(name={self.name}, id={self.id_}, protein={self.protein}, carbs={self.carbs}, fats={self.fats}, kcal={self.kcal})"

    def __eq__(self, other: "BaseProduct"):
        """
        This is the method that helps recognize two separate products with the same description as the same products.
        """
        return self.name == other.name and self.id_ == other.id_

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


class Product(BaseProduct):
    """
    This class inherits from another class (BaseProduct) and serves a point of being the real product itself.

    Args:
        mass: the mass of the product
        name: the name of the product
        id: id of the product
        protein: the amount of protein in the product
        carbs: the amount of carbs in the product
        fats: the amount of fats in the product
        kcal: the amount of kilo-calories in the product
        kwargs:
            as you like
    """

    def __init__(
        self,
        mass: float,
        name: str,
        id_: int,
        protein: float,
        carbs: float,
        fats: float,
        kcal: float | None = None,
        **kwargs,
    ):
        super().__init__(name, id_, protein, carbs, fats, kcal, **kwargs)
        self.mass = mass

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, val: float) -> None:
        if val <= 0:
            raise ValueError("Mass can't be below or can't equal 0")
        self._mass = val

    def to_protein(self):
        """this converts protein per mass to the acuall value of protein"""
        return self.protein * self.mass

    def to_carbs(self):
        """this converts carbohydrates per mass to the acuall value of protein"""
        return self.carbs * self.mass

    def to_fats(self):
        """this converts fats per mass to the acuall value of protein"""
        return self.fats * self.mass

    def to_kcal(self):
        """this converts calories per mass to the acuall value of protein"""
        return self.kcal * self.mass


if __name__ == "__main__":
    new_product = BaseProduct("ser", 1325243534, 100, 20, 25)
    sth = BaseProduct("ser", 1325243534, 10, 20, 25)
    print(new_product == sth)
