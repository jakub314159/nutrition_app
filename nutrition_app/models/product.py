from nutrition_app import database_path
from nutrition_app.error_station import error_base


class Product:
    """
    This is the blueprint to the Product.

    Attributes:
        PRODUCTS_DIR: an argument not inside the __init__ that holds the place in which the json representation files of this class will be storen.
        name(str): the name of the product.
        id_(int): the id of the product.
        protein(float): the amount of protein in the product.
        carbs(float): the amount of carbs in the product.
        fats(float): the amount of fats in the product.
        kcal(float): the amount of kilo-calories in the product.
        kwargs:
            salt: the amount of salt in the product.
            sugars: the amount of sugars in the product.
            fiber: the amount of fiber in the product.
    """

    PRODUCTS_DIR = database_path
    TABLE_NAME = "products"

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
        return f"{self.__class__.__name__}(name={self.name}, id_={self.id_}, protein={self.protein}, carbs={self.carbs}, fats={self.fats}, kcal={self.kcal})"

    def __eq__(self, other: "Product"):
        return self.name == other.name and self.kcal == other.kcal

    @property
    def protein(self) -> float:
        return self._protein

    @protein.setter
    def protein(self, value: int) -> None:
        if value < 0 or value > 100:
            raise ValueError(error_base.get("E1").format("Protein"))
        self._protein = value

    @property
    def carbs(self) -> float:
        return self._carbs

    @carbs.setter
    def carbs(self, value: int) -> None:
        if value < 0 or value > 100:
            raise ValueError(error_base.get("E1").format("Carbs"))
        self._carbs = value

    @property
    def fats(self) -> float:
        return self._fats

    @fats.setter
    def fats(self, value: int) -> None:
        if value < 0 or value > 100:
            raise ValueError(error_base.get("E1").format("Fats"))
        self._fats = value

    @property
    def kcal(self) -> float:
        return self._kcal

    @kcal.setter
    def kcal(self, value: int) -> None:
        if value is None:
            value = self.protein * 4 + self.carbs * 4 + self.fats * 9
        if value <= 0:
            raise ValueError(error_base.get("E1").format("Kcal"))

        self._kcal = value

    def to_dict(self) -> dict:
        """
        Convert Product information into a dict.

        Returns:
            dict: This returns a dict from the command vars, that is modified in a way that it could be read by a json.
        """
        return vars(self)


class EatableProduct:
    """
    This class inherits from another class (Product) and serves a point of being the real product itself.

    Attributes:
        mass(float): the mass of the product.
        product(Product): object of the class Product.
    """

    def __init__(self, mass: float, product: Product):
        self.mass = mass
        self.product = product

    def __repr__(self):
        return f"{self.__class__.__name__}(mass={self._mass}, product={self.product})"

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, val: float) -> None:
        if val <= 0:
            raise ValueError(error_base.get("E2").format("Mass"))
        self._mass = val

    @property
    def protein(self) -> float:
        return self.product.protein / 100 * self.mass

    @property
    def carbs(self) -> float:
        return self.product.carbs / 100 * self.mass

    @property
    def fats(self) -> float:
        return self.product.fats / 100 * self.mass

    @property
    def kcal(self) -> float:
        return self.product.kcal / 100 * self.mass
