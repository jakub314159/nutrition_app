import json
from pathlib import Path

from nutrition_app import database_path
from nutrition_app.error_station import error_base
from nutrition_app.sql_connector import SQLConnector


class Product:
    """
    This is the blueprint to the Product.

    Attributes:
        PRODUCTS_DIR: an argument not inside the __init__ that holds the place in which the json representation files of this class will be storen.
        name: the name of the product.
        id: id of the product.
        protein: the amount of protein in the product.
        carbs: the amount of carbs in the product.
        fats: the amount of fats in the product.
        kcal: the amount of kilo-calories in the product.
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
        return f"{self.__class__.__name__}(name={self.name}, id={self.id_}, protein={self.protein}, carbs={self.carbs}, fats={self.fats}, kcal={self.kcal})"

    def __eq__(self, other: "Product"):
        return self.name == other.name and self.id_ == other.id_

    @property
    def protein(self) -> float:
        return self._protein

    @protein.setter
    def protein(self, value) -> None:
        if value < 0 or value > 100:
            raise ValueError(error_base.get("E1").format("Protein"))
        self._protein = value

    @property
    def carbs(self) -> float:
        return self._carbs

    @carbs.setter
    def carbs(self, value) -> None:
        if value < 0 or value > 100:
            raise ValueError(error_base.get("E1").format("Carbs"))
        self._carbs = value

    @property
    def fats(self) -> float:
        return self._fats

    @fats.setter
    def fats(self, value) -> None:
        if value < 0 or value > 100:
            raise ValueError(error_base.get("E1").format("Fats"))
        self._fats = value

    @property
    def kcal(self) -> float:
        return self._kcal

    @kcal.setter
    def kcal(self, value) -> None:
        if value is None:
            value = self.protein * 4 + self.carbs * 4 + self.fats * 9
        if value <= 0:
            raise ValueError(error_base.get("E1").format("Kcal"))

        self._kcal = value

    def to_dict(self) -> dict:
        """
        This converts Product information into a dict.

        Returns:
            This returns a dict from the command vars, that is modified in a way that it could be read by a json.
        """
        vars_dict = vars(self)

        new_dict = {}
        for key, val in vars_dict.items():
            if key.startswith("_"):
                key = key[1:]
            new_dict[key] = val

        return new_dict

    # @classmethod
    # def _check_products_table(cls) -> bool:
    #     connector = SQLConnector(database_path=cls.PRODUCTS_DIR)
    #     tables = connector.get_existing_tables()
    #     return bool(tables) and cls.TABLE_NAME in tables
    #
    # def _create_products_table(self):
    #     if not self._check_products_table():
    #         connector = SQLConnector(database_path=self.PRODUCTS_DIR)
    #         connector.create_table(self.TABLE_NAME, ("id", "name", "protein", "carbs", "fats", "kcal", "salt", "sugars", "fiber"))
    #
    #
    # def save_to_sql_db(self):
    #     self._create_products_table()
    #     connector = SQLConnector(database_path=self.PRODUCTS_DIR)
    #     connector.add_to_table(self.TABLE_NAME, [(self.id_, self.name, self.protein, self.carbs, self.fats, self.kcal, self.salt, self.sugars, self.fiber)])


    @classmethod
    def from_dict(cls, input_dict: dict) -> "Product":
        """
        This reads through the dict and creates an object from the class product with the dict variables.

        Args:
            input_dict: dict that will be readen through, and from which the new Product will be created.
        Returns:
            An object class Product, that holds the values from the input_dict.
        """

        name = input_dict.get("name")
        id_ = input_dict.get("id_")
        protein = input_dict.get("protein")
        carbs = input_dict.get("carbs")
        fats = input_dict.get("fats")
        kcal = input_dict.get("kcal")

        return cls(name=name, id_=id_, protein=protein, carbs=carbs, fats=fats, kcal=kcal)

    # @classmethod
    # def from_sql_db(cls, id_: int) -> dict:
    #     connector = SQLConnector(database_path=database_path)
    #     record = connector.get_record_from_table(cls.TABLE_NAME, "id", id_)
    #     return record


    @classmethod
    def from_json_file(cls, id_: int) -> "Product":
        """
        This reads the json filed stored inside products_db and creates a class holding the same variables as the json file.

        Args:
            id_: this is the idintification number of the product.

        Returns:
            object class Product, with the same id as given.
        """
        path = cls.PRODUCTS_DIR / f"{id_}.json"
        if path.exists():
            with open(path, "r") as file:
                inside = json.load(file)
            new_object = cls.from_dict(inside)
        else:
            raise FileNotFoundError(error_base.get("E3").format(id_))

        return new_object


class EatableProduct:
    """
    This class inherits from another class (Product) and serves a point of being the real product itself.

    Attributes:
        mass: the mass of the product.
        product: object of the class Product.
    """

    def __init__(self, mass: float, product: Product):
        self.mass = mass
        self.product = product

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

    def to_dict(self):
        return self.__dict__