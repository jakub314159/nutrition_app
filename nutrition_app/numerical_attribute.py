class NumericalAttribute:
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        if type(value) not in (int, float) or value < 0:
            raise ValueError(f"{self.storage_name} must be an int or a float greater than 0")
        instance.__dict__[self.storage_name] = value
