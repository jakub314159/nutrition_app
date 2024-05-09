from nutrition_app.models.meal import Meal
from nutrition_app.user_related.user import User
from nutrition_app.user_related.daily_target import DailyTarget
from nutrition_app.models.product import EatableProduct, Product




class Day:
    def __init__(self, user: User | str, meals: dict[str, Meal] = None):
        self.meals = None or meals
        self.user = user


    def add_meal(self, meal: Meal) -> None:
        self.meals[user.meal_order[len(self.meals)]] = meal


    def list_progres(self):
        ov_kcal = sum([x.count_ov_kcal() for x in self.meals.values()])
        progres = f"{round(ov_kcal / self.user.daily_target.kcal * 100)}%"
        return progres

if __name__ == "__main__":
    product_list = [EatableProduct(mass= 100, product=Product("masło", 10, 15, 30, 40, 34)), EatableProduct(mass= 100, product=Product("ser", 10, 10, 30, 40, 34))]
    meals_dict = {"breakfast": Meal(product_list)}
    user = User(
        name="Jan", surname="Kowalski", weight=70, height=170, age=18, gender="male"
    )
    user.set_daily_target(activity=3)

    new_day = Day(meals=meals_dict, user=user)
    print(new_day.list_progres())

