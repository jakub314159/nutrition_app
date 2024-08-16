import tkinter as tk
from functools import partial
from tkinter import messagebox, Entry

from nutrition_app.app.application import (
    App,
    UsernameTakenError,
    EmailTakenError,
    IncorrectLoginInformation,
    IncorrectUsername,
)
from nutrition_app.error_station import error_base
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.work_flow.eating_day import Day


class NutritionAppGUI:
    def __init__(self, tk_root):
        self.root = tk_root
        self.root.title("Nutrition App")
        self.app = App()
        self.enable = False

        self.frames: dict[str, tk.Frame] = {
            "login": tk.Frame(root),
            "register": tk.Frame(root),
            "verification": tk.Frame(root),
            "user": tk.Frame(root),
            "target": tk.Frame(root),
            "main": tk.Frame(root),
            "meal": tk.Frame(root),
            "user_settings": tk.Frame(root),
            "target_settings": tk.Frame(root),
            "progress": tk.Frame(root),
            "id": tk.Frame(root),
            "name": tk.Frame(root),
        }

        self.entries: dict[str, tk.Entry] = {
            "log_username": tk.Entry(self.frames["login"]),
            "log_password": tk.Entry(self.frames["login"], show="*"),
            "reg_username": tk.Entry(self.frames["register"]),
            "reg_password": tk.Entry(self.frames["register"]),
            "reg_email": tk.Entry(self.frames["register"]),
            "ver_username": tk.Entry(self.frames["verification"]),
            "ver_email": tk.Entry(self.frames["verification"]),
            "ver_code": tk.Entry(self.frames["verification"]),
            "user_name": tk.Entry(self.frames["user"]),
            "user_surname": tk.Entry(self.frames["user"]),
            "protein": tk.Entry(self.frames["target"]),
            "carbs": tk.Entry(self.frames["target"]),
            "fats": tk.Entry(self.frames["target"]),
            "activity": tk.Entry(self.frames["target"]),
            "id": tk.Entry(self.frames["id"]),
            "id_mass": tk.Entry(self.frames["id"]),
            "name": tk.Entry(self.frames["name"]),
            "name_mass": tk.Entry(self.frames["name"]),
        }

        self.scales: dict[str, tk.Scale] = {
            "user_age": tk.Scale(self.frames["user"], from_=0, to=100, orient="horizontal"),
            "user_height": tk.Scale(self.frames["user"], from_=140, to=200, orient="horizontal"),
            "user_weight": tk.Scale(self.frames["user"], from_=50, to=120, orient="horizontal"),
        }

        self.users_gender = tk.StringVar(root)
        self.users_gender.set("Select gender")

        self.weight_target = tk.StringVar(root)
        self.weight_target.set("Select the type of diet")

        self.show_logins_frame()

    def enable_main_frame_features(self):
        self.app.add_day(date=Day.set_date())
        fr = self.frames["main"]

        tk.Label(fr, text=f"Date: {self.app.days_manager.days[-1].get_pretty_date()}").grid(row=0, column=3, pady=10)

        n = 1
        for meal in self.app.user.meal_order:
            tk.Label(fr, text=f"meal {n}:").grid(row=n, column=1, pady=10, padx=10)
            tk.Button(fr, text=f"{meal}", command=partial(self.show_meal_frame, meal)).grid(
                row=n, column=2, pady=10, padx=10
            )
            n += 1

        self.enable = True

    def show_main_frame(self):
        self.forget_frames()

        fr = self.frames["main"]
        fr.pack(pady=20)

        tk.Button(fr, text="User", command=self.show_user_settings_frame).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(fr, text="Target", command=self.show_target_settings_frame).grid(row=0, column=1, pady=10, padx=10)
        tk.Button(fr, text="Progress", command=self.show_progress_frame).grid(row=0, column=2, pady=10, padx=10)

    def show_user_settings_frame(self):
        self.forget_frames()

        fr = self.frames["user_settings"]
        fr.pack(pady=20)

        user = self.app.user
        user_settings_dict = {
            "name": user.name,
            "surname": user.surname,
            "age": user.age,
            "height": user.height,
            "weight": user.weight,
            "gender": user.gender,
        }

        n = 0
        for label in user_settings_dict:
            tk.Label(fr, text=f"{label}: {user_settings_dict[label]}").grid(row=n, column=0, pady=10, padx=10)
            n += 1

        tk.Button(fr, text="Change settings", command=self.show_user_frame).grid(row=7, column=0, pady=10, padx=10)
        tk.Button(fr, text="Go back", command=self.show_main_frame).grid(
            row=8,
            column=0,
            pady=10,
        )

        if self.enable:
            tk.Button(self.frames["user"], text="Go back", command=self.show_user_settings_frame).grid(
                row=7, column=0, columnspan=2, pady=10
            )

    def show_target_settings_frame(self):
        self.forget_frames()

        fr = self.frames["target_settings"]
        fr.pack(pady=20)

        target = self.app.user.daily_target
        target_settings_dict = {
            "kcal": target.kcal,
            "protein": target.protein,
            "carbs": target.carbs,
            "fats": target.fats,
        }

        n = 0
        for label in target_settings_dict:
            tk.Label(fr, text=f"{label}: {target_settings_dict[label]}").grid(
                row=n, column=0, pady=10, padx=10, columnspan=2
            )
            n += 1

        tk.Button(fr, text="Change settings", command=self.show_target_frame).grid(row=5, column=0, pady=10, padx=10)
        tk.Button(fr, text="Go back", command=self.show_main_frame).grid(row=6, column=0, pady=10, padx=10)

        if self.enable:
            tk.Button(self.frames["target"], text="Go back", command=self.show_target_settings_frame).grid(
                row=8, column=2, pady=10
            )

    def show_progress_frame(self):
        self.forget_frames()

        fr = self.frames["progress"]
        fr.pack(pady=20)

        protein = self.app.days_manager.get_progress("protein")
        carbs = self.app.days_manager.get_progress("carbs")
        fats = self.app.days_manager.get_progress("fats")
        kcal = self.app.days_manager.get_progress("kcal")

        tk.Button(fr, text=protein[0], command=partial(self.show_nutrient_frame, "protein")).grid(
            row=0, column=0, pady=10, padx=10
        )
        tk.Button(fr, text=carbs[0], command=partial(self.show_nutrient_frame, "carbs")).grid(
            row=1, column=0, pady=10, padx=10
        )
        tk.Button(fr, text=fats[0], command=partial(self.show_nutrient_frame, "fats")).grid(
            row=2, column=0, pady=10, padx=10
        )
        tk.Button(fr, text=kcal[0], command=partial(self.show_nutrient_frame, "kcal")).grid(
            row=3, column=0, pady=10, padx=10
        )

        tk.Button(fr, text="Go back", command=self.show_main_frame).grid(row=4, column=0, pady=10, padx=10)

    def show_nutrient_frame(self, nutrient_name: str):
        fr = tk.Frame(root)
        fr.pack(pady=20)

        nutrient = self.app.days_manager.get_progress(nutrient_name)
        tk.Label(fr, text=f"{nutrient_name}: {nutrient[1]}").grid(row=0, column=0, pady=10, padx=10)
        tk.Button(fr, text="Go back", command=fr.pack_forget).grid(row=1, column=0, pady=10, padx=10)

    def show_meal_frame(self, meal_name):
        self.forget_frames()

        fr = self.frames["meal"]
        fr.pack(pady=20)

        ov_dict = self.app.days_manager.get_meal_progress(meal_name)

        all_products = ""
        for name in ov_dict["names"]:
            all_products += f"{name}, "

        tk.Label(fr, text="Consumed:").grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        tk.Label(fr, text=f"protein: {ov_dict['protein']}").grid(row=1, column=0, pady=10, padx=10)
        tk.Label(fr, text=f"carbs: {ov_dict['carbs']}").grid(row=1, column=1, pady=10, padx=10)
        tk.Label(fr, text=f"fats: {ov_dict['fats']}").grid(row=1, column=2, pady=10, padx=10)
        tk.Label(fr, text=f"kcal: {ov_dict['kcal']}").grid(row=1, column=3, pady=10, padx=10)

        tk.Label(fr, text="Products names:").grid(row=2, column=1, columnspan=2, pady=10, padx=10)
        tk.Label(fr, text=f"{all_products}").grid(row=3, column=0, columnspan=4, pady=10, padx=10)

        tk.Button(fr, text="Add Product by id", command=partial(self.show_id_frame, meal_name)).grid(
            row=4, column=0, columnspan=2, pady=10, padx=10
        )
        tk.Button(fr, text="Add Product by name", command=partial(self.show_name_frame, meal_name)).grid(
            row=4, column=2, columnspan=2, pady=10, padx=10
        )

        tk.Button(fr, text="Go back", command=self.show_main_frame).grid(
            row=5, column=1, columnspan=2, pady=10, padx=10
        )

    def show_id_frame(self, meal_name):
        self.forget_frames()

        fr = self.frames["id"]
        fr.pack(pady=20)

        tk.Label(fr, text="Products id:").grid(row=0, column=0, pady=10, padx=10)
        self.entries["id"].grid(row=1, column=0, pady=10, padx=10)

        tk.Label(fr, text="Products mass:").grid(row=0, column=1, pady=10, padx=10)
        self.entries["id_mass"].grid(row=1, column=1, pady=10, padx=10)

        tk.Button(fr, text="Add product", command=partial(self.add_product_by_id_to_meal, meal_name)).grid(
            row=2, column=0, columnspan=2, pady=10, padx=10
        )
        tk.Button(fr, text="Go back", command=partial(self.show_meal_frame, meal_name)).grid(
            row=3, column=0, columnspan=2, pady=10, padx=10
        )

    def add_product_by_id_to_meal(self, meal_name):
        products_id = int(self.entries["id"].get())
        products_mass = int(self.entries["id_mass"].get())
        index = int(self.app.user.meal_order.index(meal_name))

        try:
            self.app.add_product_by_id_to_meal(index=index, id_=products_id, mass=products_mass)
            messagebox.showinfo(title="error", message="Product added")
        except Exception:
            messagebox.showerror(title="error", message="Wrong input")

    def show_name_frame(self, meal_name):
        self.forget_frames()

        fr = self.frames["name"]
        fr.pack(pady=20)

        tk.Label(fr, text="Products name:").grid(row=0, column=0, pady=10, padx=10)
        self.entries["name"].grid(row=1, column=0, pady=10, padx=10)

        tk.Label(fr, text="Products mass:").grid(row=0, column=1, pady=10, padx=10)
        self.entries["name_mass"].grid(row=1, column=1, pady=10, padx=10)

        tk.Button(fr, text="Add product", command=partial(self.add_product_by_name_to_meal, meal_name)).grid(
            row=2, column=0, columnspan=2, pady=10, padx=10
        )
        tk.Button(fr, text="Go back", command=partial(self.show_meal_frame, meal_name)).grid(
            row=3, column=0, columnspan=2, pady=10, padx=10
        )

    def add_product_by_name_to_meal(self, meal_name):
        products_name = str(self.entries["name"].get())
        products_mass = int(self.entries["name_mass"].get())
        index = int(self.app.user.meal_order.index(meal_name))

        try:
            self.app.add_product_by_name_to_meal(index=index, name=products_name, mass=products_mass)
            messagebox.showinfo(title="error", message="Product added")
        except Exception:
            messagebox.showerror(title="error", message="Wrong input")

    def forget_frames(self):
        for frame in self.frames:
            self.frames[frame].pack_forget()

    def show_logins_frame(self):
        self.forget_frames()

        fr = self.frames["login"]
        fr.pack(pady=20)

        tk.Label(fr, text="Username:").grid(row=0, column=0, pady=10, padx=10)
        self.entries["log_username"].grid(row=0, column=1, pady=10, padx=10)

        tk.Label(fr, text="Password").grid(row=1, column=0, pady=10, padx=10)
        self.entries["log_password"].grid(row=1, column=1, pady=10, padx=10)

        tk.Button(fr, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        tk.Button(fr, text="Register", command=self.show_register_frame).grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.entries["log_username"].get()
        password = self.entries["log_password"].get()

        try:
            self.app.login(username, password)

            if self.app.user is None:
                messagebox.showinfo(message="Please create a new user")
                self.show_user_frame()

            elif self.app.user.daily_target == DailyTarget():
                messagebox.showinfo(message="Please create a daily target")
                self.show_target_frame()

            else:
                messagebox.showinfo(title="User", message="User is being loaded")
                self.enable_main_frame_features()
                self.show_main_frame()
        except IncorrectUsername:
            messagebox.showerror(title="Error", message="Incorrect username given")
        except IncorrectLoginInformation:
            messagebox.showerror(title="Error", message="Incorrect login information.")

    def show_register_frame(self):
        self.forget_frames()

        fr = self.frames["register"]
        fr.pack(pady=20)

        tk.Label(fr, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.entries["reg_username"].grid(row=0, column=1, padx=5, pady=5)

        tk.Label(fr, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.entries["reg_password"].grid(row=1, column=1, padx=5, pady=5)

        tk.Label(fr, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.entries["reg_email"].grid(row=2, column=1, padx=5, pady=5)

        tk.Button(fr, text="Register", command=self.register).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(fr, text="automatic pass", command=self.create_automatic_password).grid(
            row=4, column=0, columnspan=2, pady=10
        )
        tk.Button(fr, text="Back to Login", command=self.show_logins_frame).grid(row=5, column=0, columnspan=2, pady=10)

    def register(self):
        username = self.entries["reg_username"].get()
        password = self.entries["reg_password"].get()
        email = self.entries["reg_email"].get()

        try:
            self.app.register(username, password, email)
            messagebox.showinfo("Success", "Registration successful\nPlease verify your email address.")
            self.show_verification_frame()
        except UsernameTakenError:
            messagebox.showerror("Error", "Username is taken.")
        except EmailTakenError:
            messagebox.showerror("Error", "Email is taken.")

    def create_automatic_password(self):
        automatic_pass = self.app.automatic_password()
        self.entries["reg_password"].delete(0, "end")
        self.entries["reg_password"].insert(index=0, string=automatic_pass)

    def show_verification_frame(self):
        self.forget_frames()

        fr = self.frames["verification"]
        fr.pack(pady=20)

        tk.Label(fr, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.entries["ver_username"].grid(row=0, column=1, padx=5, pady=5)

        tk.Label(fr, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.entries["ver_email"].grid(row=1, column=1, padx=5, pady=5)

        tk.Label(fr, text="Code:").grid(row=2, column=0, padx=5, pady=5)
        self.entries["ver_code"].grid(row=2, column=1, padx=5, pady=5)

        tk.Button(fr, text="Verify", command=self.verify).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(fr, text="Back to Login", command=self.show_logins_frame).grid(row=4, column=0, columnspan=2, pady=10)

    def verify(self):
        try:
            self.app.verify(
                username=self.entries["ver_username"].get(),
                email=self.entries["ver_email"].get(),
                code=self.entries["ver_code"].get(),
            )
            self.show_logins_frame()
        except ValueError:
            messagebox.showerror(title="Error", message=error_base.get("E14"))

    def show_user_frame(self):
        self.forget_frames()

        fr = self.frames["user"]
        fr.pack(pady=20)

        self.entries["user_name"].insert(0, "your name")
        self.entries["user_name"].grid(row=0, column=1, padx=5, pady=5)

        self.entries["user_surname"].insert(0, "your surname")
        self.entries["user_surname"].grid(row=1, column=1, padx=5, pady=5)

        tk.Label(fr, text="Age:").grid(row=2, column=0, padx=5, pady=5)
        self.scales["user_age"].grid(row=2, column=1, padx=5, pady=5)

        tk.Label(fr, text="Height(cm):").grid(row=3, column=0, padx=5, pady=5)
        self.scales["user_height"].grid(row=3, column=1, padx=5, pady=5)

        tk.Label(fr, text="Weight(kg):").grid(row=4, column=0, padx=5, pady=5)
        self.scales["user_weight"].grid(row=4, column=1, padx=5, pady=5)

        users_gender_switch = tk.OptionMenu(fr, self.users_gender, "male", "female")
        users_gender_switch.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(fr, text="Create user", command=self.create_user).grid(row=6, column=0, columnspan=2, pady=10)

    def create_user(self):
        self.app.create_user(
            self.entries["user_name"].get(),
            self.entries["user_surname"].get(),
            self.scales["user_age"].get(),
            self.scales["user_height"].get(),
            self.scales["user_weight"].get(),
            self.users_gender.get(),
        )
        self.show_target_frame()

    def show_target_frame(self):
        self.forget_frames()

        fr = self.frames["target"]
        fr.pack(pady=20)

        tk.Label(fr, text="Set micronutrients ").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(fr, text="Protein:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(fr, text="Carbs:").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(fr, text="Fats:").grid(row=6, column=0, padx=5, pady=5)
        tk.Label(fr, text="Please choose one of the options:").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(fr, text="Set activity (1 - 5)").grid(row=1, column=2, padx=5, pady=5)

        self.entries["protein"].grid(row=3, column=0, padx=5, pady=5)
        self.entries["carbs"].grid(row=5, column=0, padx=5, pady=5)
        self.entries["fats"].grid(row=7, column=0, padx=5, pady=5)
        self.entries["activity"].grid(row=3, column=2, padx=5, pady=5)

        users_target_switch = tk.OptionMenu(fr, self.weight_target, "lose weight", "maintain weight", "gain weight")
        users_target_switch.grid(row=6, column=2, padx=5, pady=5)

        tk.Button(fr, text="Create daily target", command=self.create_daily_target).grid(row=7, column=2, pady=10)

    def create_daily_target(self):
        protein = self.entries["protein"].get()
        carbs = self.entries["carbs"].get()
        fats = self.entries["fats"].get()
        activity = self.entries["activity"].get()
        target = self.weight_target.get()

        if protein and carbs and fats:
            kcal = protein * 4 + carbs * 4 + fats * 9
            self.app.create_daily_target(kcal=float(kcal), protein=float(protein), carbs=float(carbs), fats=float(fats))
        else:
            self.app.create_daily_target(int(activity))

        if target == "loose weight":
            self.app.user.daily_target.kcal -= 140
            self.app.user.daily_target.protein -= 10
            self.app.user.daily_target.carbs -= 10
            self.app.user.daily_target.fats -= 10

        elif target == "gain weight":
            self.app.user.daily_target.kcal += 140
            self.app.user.daily_target.protein += 10
            self.app.user.daily_target.carbs += 10
            self.app.user.daily_target.fats += 10

        self.enable_main_frame_features()
        self.show_main_frame()


if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionAppGUI(root)
    root.mainloop()
