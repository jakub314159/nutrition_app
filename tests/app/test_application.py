import json
from pathlib import Path
from pytest import fixture, raises
from base64 import b64encode


from nutrition_app.app.application import App, UsernameTakenError, EmailTakenError, WrongMadePasswordError, IncorrectLoginInformation
from nutrition_app.user.daily_target import DailyTarget

LOGIN_DIRPATH = Path(__file__).parent.parent / "test_db" / "test_login_base.json"
USER_DIRPATH = Path(__file__).parent.parent / "test_db" / "test_user_base.json"


@fixture()
def app():
    app = App()
    return app





class TestApp:
    def test_repr(self, app):
        assert app.__repr__() == f"{app.__class__.__name__}()"

    def test_delete_account(self, app):
        app.register("1", "Ab1@cdefgh", "3", LOGIN_DIRPATH)
        with open(LOGIN_DIRPATH, "r") as file:
            numer = len(json.load(file)["users"])
        app.delete_account(1, LOGIN_DIRPATH)
        with open(LOGIN_DIRPATH, "r") as file:
            new_numer = len(json.load(file)["users"])
        assert numer == new_numer + 1

    def test_check_password_to_low_char(self, app):
        with raises(expected_exception=WrongMadePasswordError):
            app.check_password("A1@b")

    def test_check_password_to_much_char(self, app):
        with raises(expected_exception=WrongMadePasswordError):
            app.check_password("A1@bcesdfgaeihuxUyy^$%D122")

    def test_check_password_all_upper(self, app):
        with raises(expected_exception=WrongMadePasswordError):
            app.check_password("A1@BCDEFGHI")

    def test_check_password_all_lower(self, app):
        with raises(expected_exception=WrongMadePasswordError):
            app.check_password("a1@bcdefghi")

    def test_check_password_no_num(self, app):
        with raises(expected_exception=WrongMadePasswordError):
            app.check_password("A@BCDEFghIJ")

    def test_check_password_no_special_char(self, app):
        with raises(expected_exception=WrongMadePasswordError):
            app.check_password("A1BCDEfgHIJ")

    def test_check_password_all_num_or_special(self, app):
        with raises(expected_exception=WrongMadePasswordError):
            app.check_password("1234^$&$%23^$")

    def test_register_username_taken_error(self, app):
        with raises(expected_exception=UsernameTakenError):
            app.register("user", "Ab1@cdefgh", "email.com", LOGIN_DIRPATH)

    def test_register_email_taken_error(self, app):
        with raises(expected_exception=EmailTakenError):
            app.register("1", "Ab1@cdefgh", "email.com", LOGIN_DIRPATH)

    def test_register(self, app):
        username="1"
        password="Ab1@cdefgh"
        email="3"
        app.register(username=username, password=password, email=email, dirpath=LOGIN_DIRPATH)

        with open(LOGIN_DIRPATH, "r") as file:
            inside = json.load(file)

        app.delete_account(1, LOGIN_DIRPATH)

        assert inside["users"][1]["username"] == username and inside["users"][1]["password"] == b64encode(password.encode("utf-8")).decode("utf-8") and inside["users"][1]["email"] == b64encode(email.encode("utf-8")).decode("utf-8")

    def test_login_incorrect_username(self, app):
        with raises(expected_exception=IncorrectLoginInformation):
            app.login("1", "1234")

    def test_login_incorrect_passowrd(self, app):
        with raises(expected_exception=IncorrectLoginInformation):
            app.login("user", "password")

    def test_login(self, app):
        app.login(username="user", password="Ab1@cdefgh", dirpath= LOGIN_DIRPATH)
        assert app.username == "user" and app.password == "Ab1@cdefgh"

    def test_reload_base(self, app):
        user_dict = {"test": "1"}

        with open(USER_DIRPATH, "r") as file:
            inside = json.load(file)

        app.reload_base(user_dict, USER_DIRPATH)

        with open(USER_DIRPATH, "r") as file:
            new = json.load(file)

        assert len(new["users"]) == len(inside["users"]) + 1

    def test_create_user(self, app):
        app.login(username="user", password="Ab1@cdefgh", dirpath= LOGIN_DIRPATH)
        app.create_user("jan", "kowalski", 18, 180, 70, "male", DailyTarget(), USER_DIRPATH)

        with open(USER_DIRPATH, "r") as file:
            new = json.load(file)

        usernames = [x['user'] for x in new["users"] if x['username'] == "user"]

        filler = {
            "users": [
            ]
        }

        with open(USER_DIRPATH, "w") as file:
            json.dump(filler, file, indent=4)

        assert usernames[0]["name"] == "jan" and usernames[0]["surname"] == "kowalski"






