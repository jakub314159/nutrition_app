from abc import ABC, abstractmethod


class Figure(ABC):

    def __repr__(self) -> str:
        """a=5, b=4, ..."""
        params = ", ".join([f"{key}={val}" for key, val in self.__dict__.items()])
        ret = f"{self.__class__.__name__}({params})"
        return ret

    @abstractmethod
    def calculate_area(self) -> float:
        """Calculate area"""

    @abstractmethod
    def calculate_circumference(self) -> float:
        """Calculate circumference"""


class Rectangle(Figure):
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def calculate_area(self) -> float:
        """Calculate rectangle area"""
        return self.a * self.b

    def calculate_circumference(self) -> float:
        """Calculate circumference"""
        return 2 * self.a + 2 * self.b


class Square(Figure):
    def __init__(self, a: float):
        self.a = a

    def calculate_area(self) -> float:
        """Calculate rectangle area"""
        return self.a ** 2

    def calculate_circumference(self) -> float:
        """Calculate circumference"""
        return 4 * self.a


class Triangle(Figure):
    def __init__(self, a: float, h: float, b: float, c: float):
        self.a = a
        self.h = h
        self.b = b
        self.c = c

    def calculate_area(self) -> float:
        """Calculate rectangle area"""
        return (self.a * self.h) / 2

    def calculate_circumference(self) -> float:
        """Calculate circumference"""
        return self.a + self.b + self.c


def foo(fig: Figure) -> float:
    return fig.calculate_area()


if __name__ == "__main__":
    rectangle = Rectangle(5, 10)
    print(rectangle)

    triangle = Triangle(5, 3, 3, 4)
    print(triangle)

    foo(triangle)
