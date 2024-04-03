import json
from pathlib import Path

from nutrition_app import products_dir


class Product:
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

    def __eq__(self, other: "Product"):
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

    def to_dict(self) -> dict:
        return vars(self)

    def to_json_file(self):
        inside = self.to_dict()
        name = f"{self.id_}.json"

        path = products_dir / name

        if path.exists():
            raise FileExistsError("This id is already taken")

        with open(path, "w") as file:
            json.dump(inside, file)


    @classmethod
    def from_dict(cls, input_dict: dict) -> 'Product':
        name = input_dict.get("name")
        id_ = input_dict.get("id_")
        protein = input_dict.get("protein")
        carbs = input_dict.get("carbs")
        fats = input_dict.get("fats")
        kcal = input_dict.get("kcal")

        return cls(name=name, id_=id_, protein=protein, carbs=carbs, fats=fats, kcal=kcal)



    @classmethod
    def from_json_file(cls, id_: int):
        path = products_dir / f"{id_}.json"
        if path.exists():
            with open(path, "r") as file:
                inside = json.load(file)
            cls.from_dict(inside)
        else:
            raise FileNotFoundError(f"There is no such file named {id_}")







class EatableProduct:
    """
    This class inherits from another class (Product) and serves a point of being the real product itself.

    Args:
        mass: the mass of the product
        product: object of the class Product
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
            raise ValueError("Mass can't be below or can't equal 0")
        self._mass = val

    def to_protein(self):
        """this converts protein per mass to the acuall value of protein"""
        return self.product.protein * self.mass

    def to_carbs(self):
        """this converts carbohydrates per mass to the acuall value of protein"""
        return self.product.carbs * self.mass

    def to_fats(self):
        """this converts fats per mass to the acuall value of protein"""
        return self.product.fats * self.mass

    def to_kcal(self):
        """this converts calories per mass to the acuall value of protein"""
        return self.product.kcal * self.mass


if __name__ == "__main__":
    new_product = Product("ser", 1325243534, 100, 20, 25)
    sth = Product("ser", 1325243534, 10, 20, 25)
    print(new_product == sth)
