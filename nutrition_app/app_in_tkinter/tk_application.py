import tkinter as tk
from tkinter import messagebox
from typing import Any

from nutrition_app.app.application import App, UsernameTakenError, EmailTakenError, IncorrectLoginInformation, IncorrectUsername
from nutrition_app.error_station import error_base
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.work_flow.eating_day import Day


class NutritionAppGUI:
    def __init__(self, tk_root):
        self.root = tk_root
        self.root.title("Nutrition App")
        self.app = App()
        self.main_frame = tk.Frame(root)
        self.meal_frame = tk.Frame(root)
        self.user_settings_frame = tk.Frame(root)
        self.target_settings_frame = tk.Frame(root)
        self.progress_frame = tk.Frame(root)

        #login
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.log_username_entry = tk.Entry(self.login_frame)
        self.log_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.log_password_entry = tk.Entry(self.login_frame, show="*")
        self.log_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.login_frame, text="Register", command=self.show_registration_frame).grid(row=3, column=0, columnspan=2, pady=10)

        #register
        self.registration_frame = tk.Frame(root)

        tk.Label(self.registration_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_username_entry = tk.Entry(self.registration_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.registration_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = tk.Entry(self.registration_frame)
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.registration_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_email_entry = tk.Entry(self.registration_frame)
        self.reg_email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.registration_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.registration_frame, text="automatic pass", command=self.create_automatic_password).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.registration_frame, text="Back to Login", command=self.show_login_frame).grid(row=5, column=0, columnspan=2, pady=10)



        #verify
        self.verification_frame = tk.Frame(root)

        tk.Label(self.verification_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.ver_username_entry = tk.Entry(self.verification_frame)
        self.ver_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.verification_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.ver_email_entry = tk.Entry(self.verification_frame)
        self.ver_email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.verification_frame, text="Code:").grid(row=2, column=0, padx=5, pady=5)
        self.ver_code_entry = tk.Entry(self.verification_frame)
        self.ver_code_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.verification_frame, text="Verify", command=self.verify).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.verification_frame, text="Back to Login", command=self.show_login_frame).grid(
            row=4, column=0, columnspan=2, pady=10
        )


        #user
        self.user_frame = tk.Frame(root)

        self.user_name_entry = tk.Entry(self.user_frame)
        self.user_name_entry.insert(0, "your name")
        self.user_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.user_surname_entry = tk.Entry(self.user_frame)
        self.user_surname_entry.insert(0, "your surname")
        self.user_surname_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.user_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5)
        self.user_age_zipper = tk.Scale(self.user_frame, from_=0, to=100, orient="horizontal")
        self.user_age_zipper.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.user_frame, text="Height(cm):").grid(row=3, column=0, padx=5, pady=5)
        self.user_height_zipper = tk.Scale(self.user_frame, from_=140, to=200, orient="horizontal")
        self.user_height_zipper.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.user_frame, text="Weight(kg):").grid(row=4, column=0, padx=5, pady=5)
        self.user_weight_zipper = tk.Scale(self.user_frame, from_=40, to=140, orient="horizontal")
        self.user_weight_zipper.grid(row=4, column=1, padx=5, pady=5)

        self.users_gender = tk.StringVar(root)
        self.users_gender.set("Select gender")
        self.users_gender_switch = tk.OptionMenu(self.user_frame, self.users_gender, "male", "female")
        self.users_gender_switch.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.user_frame, text="Create user", command=self.create_user).grid(row=6, column=0, columnspan=2, pady=10)


        #target
        self.target_frame = tk.Frame(root)

        tk.Label(self.target_frame, text= "Set micronutrients ").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self.target_frame, text= "Protein:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self.target_frame, text= "Carbs:").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(self.target_frame, text= "Fats:").grid(row=6, column=0, padx=5, pady=5)
        tk.Label(self.target_frame, text= "Please choose one of the options:").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.target_frame, text= "Set activity (1 - 5)").grid(row=1, column=2, padx=5, pady=5)

        self.protein =  tk.Entry(self.target_frame)
        self.protein.grid(row=3, column=0, padx=5, pady=5)

        self.carbs =  tk.Entry(self.target_frame)
        self.carbs.grid(row=5, column=0, padx=5, pady=5)

        self.fats = tk.Entry(self.target_frame)
        self.fats.grid(row=7, column=0, padx=5, pady=5)

        self.activity = tk.Entry(self.target_frame)
        self.activity.grid(row=3, column=2, padx=5, pady=5)

        self.weight_target = tk.StringVar(root)
        self.weight_target.set("Select the type of diet")
        self.users_target_switch = tk.OptionMenu(self.target_frame, self.weight_target, "lose weight", "maintain weight", "gain weight")
        self.users_target_switch.grid(row=6, column=2, padx=5, pady=5)
        
        tk.Button(self.target_frame, text="Create daily target", command=self.create_daily_target).grid(row=7, column=2, pady=10)


        tk.Button(self.main_frame, text="User", command=self.user_settings).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self.main_frame, text="Target", command=self.target_settings).grid(row=0, column=1, pady=10, padx=10)
        tk.Button(self.main_frame, text="Progress", command=self.show_progress).grid(row=0, column=2, pady=10, padx=10)


    def show_login_frame(self):
        self.verification_frame.pack_forget()
        self.registration_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def show_registration_frame(self):
        self.login_frame.pack_forget()
        self.registration_frame.pack(pady=20)

    def show_verification_frame(self):
        self.registration_frame.pack_forget()
        self.verification_frame.pack(pady=20)

    def show_user_frame(self):
        self.user_settings_frame.pack_forget()
        self.main_frame.pack_forget()
        self.login_frame.pack_forget()
        self.verification_frame.pack_forget()
        self.user_frame.pack(pady=20)

    def show_target_frame(self):
        self.target_settings_frame.pack_forget()
        self.main_frame.pack_forget()
        self.login_frame.pack_forget()
        self.user_frame.pack_forget()
        self.target_frame.pack(pady=20)

    def show_main_frame(self):
        self.meal_frame.pack_forget()
        self.progress_frame.pack_forget()
        self.login_frame.pack_forget()
        self.target_frame.pack_forget()
        self.user_settings_frame.pack_forget()
        self.target_settings_frame.pack_forget()
        self.main_frame.pack(pady=20)

    def enable_main_frame_features(self):
        self.app.add_day(date=Day.set_date())
        tk.Label(self.main_frame, text=f"Date: {self.app.days_manager.days[-1].get_pretty_date()}").grid(row=0, column=3, pady=10)



        tk.Label(self.main_frame, text="meal 1:").grid(row=1, column=1, pady=10, padx=10)
        tk.Button(self.main_frame, text=f"{self.app.user.meal_order[0]}", command=self.get_meal1).grid(row=1, column=2, pady=10, padx=10)


        tk.Label(self.main_frame, text="meal 2:").grid(row=2, column=1, pady=10, padx=10)
        tk.Button(self.main_frame, text=f"{self.app.user.meal_order[1]}", command=self.get_meal2).grid(row=2, column=2, pady=10, padx=10)

        tk.Label(self.main_frame, text="meal 3:").grid(row=3, column=1, pady=10, padx=10)
        tk.Button(self.main_frame, text=f"{self.app.user.meal_order[2]}", command=self.get_meal3).grid(
            row=3, column=2, pady=10, padx=10
        )

        tk.Label(self.main_frame, text="meal 4:").grid(row=4, column=1, pady=10, padx=10)
        tk.Button(self.main_frame, text=f"{self.app.user.meal_order[3]}", command=self.get_meal4).grid(
            row=4, column=2, pady=10, padx=10
        )

        tk.Button(self.user_frame, text="Go back", command=self.show_user_settings_frame).grid(
            row=7, column=0, columnspan=2, pady=10
        )

        tk.Button(self.target_frame, text="Go back", command=self.show_target_settings_frame).grid(row=8, column=2, pady=10)

    def get_meal1(self):
        self.get_meal(self.app.user.meal_order[0])

    def get_meal2(self):
        self.get_meal(self.app.user.meal_order[1])

    def get_meal3(self):
        self.get_meal(self.app.user.meal_order[2])

    def get_meal4(self):
        self.get_meal(self.app.user.meal_order[3])

    def show_user_settings_frame(self):
        self.user_frame.pack_forget()
        self.main_frame.pack_forget()
        self.user_settings_frame.pack(pady=20)

    def show_target_settings_frame(self):
        self.target_frame.pack_forget()
        self.main_frame.pack_forget()
        self.target_settings_frame.pack(pady=20)

    def show_progress_frame(self):
        self.main_frame.pack_forget()
        self.progress_frame.pack(pady=20)

    def create_automatic_password(self):
        automatic_pass = self.app.automatic_password()
        self.reg_password_entry.delete(0, "end")
        self.reg_password_entry.insert(index=0, string=automatic_pass)

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        email = self.reg_email_entry.get()

        try:
            self.app.register(username, password, email)
            messagebox.showinfo("Success", "Registration successful\nPlease verify your email address.")
            self.show_verification_frame()
        except UsernameTakenError:
            messagebox.showerror("Error", "Username is taken.")
        except EmailTakenError:
            messagebox.showerror("Error", "Email is taken.")

    def verify(self):
        username = self.ver_username_entry.get()
        email = self.ver_email_entry.get()
        code = self.ver_code_entry.get()

        try:
            self.app.verify(username, email, code)
            self.show_login_frame()
        except ValueError:
            messagebox.showerror(title="Error", message=error_base.get("E14"))

    def login(self):
        username = self.log_username_entry.get()
        password = self.log_password_entry.get()

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
            messagebox.showerror(title="Error",  message="Incorrect login information.")

    def create_user(self):
        name = self.user_name_entry.get()
        surname = self.user_surname_entry.get()
        age = self.user_age_zipper.get()
        height = self.user_height_zipper.get()
        weight = self.user_weight_zipper.get()
        gender = self.users_gender.get()


        self.app.create_user(name, surname, age, height, weight, gender)
        self.show_target_frame()

    def create_daily_target(self):
        protein = self.protein.get()
        carbs = self.carbs.get()
        fats = self.fats.get()
        activity = self.activity.get()

        target = self.weight_target.get()

        if target == "gain weight":
            protein += protein / 10
            carbs += carbs / 10
            fats += fats / 10

        elif target == "loose weight":
            protein -= protein / 10
            carbs -= carbs / 10
            fats -= fats / 10

        if protein and carbs and fats:
            kcal = protein * 4 + carbs * 4 + fats * 9
            self.app.create_daily_target(kcal=kcal, protein=protein, carbs=carbs, fats=fats)
        else:
            self.app.create_daily_target(activity)
        self.enable_main_frame_features()
        self.show_main_frame()

    def user_settings(self):
        self.show_user_settings_frame()
        user = self.app.user
        user_settings_dict = {"name": user.name, "surname": user.surname, "age": user.age, "height": user.height, "weight": user.weight, "gender": user.gender}

        n = 0
        for label in user_settings_dict:
            tk.Label(self.user_settings_frame, text=f"{label}: {user_settings_dict[label]}").grid(row=n, column=0, pady=10, padx=10)
            n += 1

        tk.Button(self.user_settings_frame, text="Change settings", command=self.show_user_frame).grid(row=7, column=0, pady=10, padx=10)
        tk.Button(self.user_settings_frame, text="Go back", command=self.show_main_frame).grid(row=8, column=0, pady=10, padx=10)

    def target_settings(self):
        self.show_target_settings_frame()
        target = self.app.user.daily_target
        target_settings_dict = {"kcal": target.kcal, "protein": target.protein, "carbs": target.carbs, "fats": target.fats}

        n = 0
        for label in target_settings_dict:
            tk.Label(self.target_settings_frame, text=f"{label}: {target_settings_dict[label]}").grid(row=n, column=0, pady=10, padx=10, columnspan=2)
            n += 1


        tk.Button(self.target_settings_frame, text="Change settings", command=self.show_target_frame).grid(row=5, column=0, pady=10, padx=10)
        tk.Button(self.target_settings_frame, text="Go back", command=self.show_main_frame).grid(row=6, column=0, pady=10, padx=10)


    def show_progress(self):
        self.show_progress_frame()
        protein = self.app.days_manager.get_progress("protein")
        carbs = self.app.days_manager.get_progress("carbs")
        fats = self.app.days_manager.get_progress("fats")
        kcal = self.app.days_manager.get_progress("kcal")

        tk.Button(self.progress_frame, text=protein[0], command= self.show_protein_frame).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self.progress_frame, text=carbs[0], command= self.show_carbs_frame).grid(row=1, column=0, pady=10, padx=10)
        tk.Button(self.progress_frame, text=fats[0], command= self.show_fats_frame).grid(row=2, column=0, pady=10, padx=10)
        tk.Button(self.progress_frame, text=kcal[0], command= self.show_kcal_frame).grid(row=3, column=0, pady=10, padx=10)

        tk.Button(self.progress_frame, text="Go back", command=self.show_main_frame).grid(row=4, column=0, pady=10, padx=10)

    def show_protein_frame(self):
        var_frame = tk.Frame(root)
        var_frame.pack(pady=20)

        protein = self.app.days_manager.get_progress("protein")

        tk.Label(var_frame, text=f"protein: {protein[1]}").grid(row=0, column=0, pady=10, padx=10)

        tk.Button(var_frame, text="Go back", command=var_frame.pack_forget).grid(row=1, column=0, pady=10, padx=10)

    def show_carbs_frame(self):
        var_frame = tk.Frame(root)
        var_frame.pack(pady=20)

        carbs = self.app.days_manager.get_progress("carbs")

        tk.Label(var_frame, text=f"carbs: {carbs[1]}").grid(row=0, column=0, pady=10, padx=10)

        tk.Button(var_frame, text="Go back", command=var_frame.pack_forget).grid(row=1, column=0, pady=10, padx=10)

    def show_fats_frame(self):
        var_frame = tk.Frame(root)
        var_frame.pack(pady=20)

        fats = self.app.days_manager.get_progress("fats")

        tk.Label(var_frame, text=f"fats: {fats[1]}").grid(row=0, column=0, pady=10, padx=10)

        tk.Button(var_frame, text="Go back", command=var_frame.pack_forget).grid(row=1, column=0, pady=10, padx=10)

    def show_kcal_frame(self):
        var_frame = tk.Frame(root)
        var_frame.pack(pady=20)

        kcal = self.app.days_manager.get_progress("kcal")

        tk.Label(var_frame, text=f"kcal: {kcal[1]}").grid(row=0, column=0, pady=10, padx=10)

        tk.Button(var_frame, text="Go back", command=var_frame.pack_forget).grid(row=1, column=0, pady=10, padx=10)


    def show_meal_frame(self):
        self.main_frame.pack_forget()
        self.meal_frame.pack(pady=20)

    def get_meal(self, meal_name):
        self.show_meal_frame()

        ov_dict = self.app.days_manager.get_meal_progress(meal_name)

        all_products = ""
        for name in ov_dict["names"]:
            all_products += f"{name}, "

        tk.Label(self.meal_frame, text="Consumed:").grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        tk.Label(self.meal_frame, text=f"protein: {ov_dict['protein']}").grid(row=1, column=0, pady=10, padx=10)
        tk.Label(self.meal_frame, text=f"carbs: {ov_dict['carbs']}").grid(row=1, column=1, pady=10, padx=10)
        tk.Label(self.meal_frame, text=f"fats: {ov_dict['fats']}").grid(row=1, column=2, pady=10, padx=10)
        tk.Label(self.meal_frame, text=f"kcal: {ov_dict['kcal']}").grid(row=1, column=3, pady=10, padx=10)

        tk.Label(self.meal_frame, text="Products names:").grid(row=2, column=1, columnspan=2, pady=10, padx=10)
        tk.Label(self.meal_frame, text=f"{all_products}").grid(row=3, column=0, columnspan=4, pady=10, padx=10)

        tk.Button(self.meal_frame, text="Get Product by id").grid(row=4, column=0, columnspan=2, pady=10, padx=10)
        self.id_entry = tk.Entry(self.meal_frame)
        self.id_entry.insert(0, "Products id")
        self.id_entry.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

        tk.Button(self.meal_frame, text="Get Product by name").grid(row=4, column=2, columnspan=2, pady=10, padx=10)
        self.name_entry = tk.Entry(self.meal_frame)
        self.name_entry.insert(0, "Products name")
        self.name_entry.grid(row=5, column=2, columnspan=2, pady=10, padx=10)

        tk.Button(self.meal_frame, text="Go back", command=self.show_main_frame).grid(row=6, column=1, columnspan=2, pady=10, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionAppGUI(root)
    root.mainloop()