import json
from pathlib import Path
from pytest import fixture, raises
from base64 import b64encode


from nutrition_app.app.application import App, UsernameTakenError, EmailTakenError, WrongMadePasswordError, IncorrectLoginInformation
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.sql_connector import SQLConnector
from tests.mocked_connector import MockedConnector

LOGIN_DIRPATH = Path(__file__).parent.parent / "test_db" / "test_login_base.json"
USER_DIRPATH = Path(__file__).parent.parent / "test_db" / "test_user_base.json"


LOGIN_SQL_PATH = Path(__file__).parent.parent / "test_db" / "test_nutrition_app_database.db"

@fixture()
def app():
    app = App("logins", database_connector=MockedConnector())
    app.DATABASE_DIR = Path(__file__).parent.parent / "test_db" / "test_nutrition_app_database.db"
    return app


class TestApp:
    def test_repr(self, app):
        assert app.__repr__() == f"{app.__class__.__name__}()"

    def test_delete_account(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email"))
        app.register("1", "Ab1@cdefgh", "3")
        old_val = app.database_connector.get_record_from_table("logins", "username", "1")

        app.delete_account("logins", "username", "1")
        new_val = app.database_connector.get_existing_tables()

        assert old_val["username"] == "1" and "1" not in new_val


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
            app.database_connector.create_table("logins", ("username", "password", "email"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.register("test", "Ab1@cdefgh", "email.com")


    def test_register_username_taken_error(self, app):
        with raises(expected_exception=EmailTakenError):
            app.database_connector.create_table("logins", ("username", "password", "email"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.register("user", "Ab1@cdefgh", "gmail.com")

    def test_check_products_table(self, app):
        val = app._check_products_table()
        assert val == False

    def test_create_products_table(self, app):
        app._create_products_table()
        val = app._check_products_table()
        assert val == True

    def test_save_to_sql_db(self, app):
        app.save_to_sql_db("nie", "tak", "no")
        sql_dict = app.database_connector.get_table("logins")
        assert sql_dict["email"][0] == "no" and sql_dict["password"][0] == "tak" and sql_dict["username"][0] == "nie"


    def test_register(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email"))
        app.register("test", "Ab1@cdefgh", "gmail.com")

        sql_dict = app.database_connector.get_table("logins")

        assert sql_dict["username"][0] == "test" and sql_dict["password"][0] == "Ab1@cdefgh" and sql_dict["email"][0] == "gmail.com"


    def test_login_incorrect_username(self, app):
        with raises(expected_exception=IncorrectLoginInformation):
            app.database_connector.create_table("logins", ("username", "password", "email"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.login("test1", "Ab1@cdefgh")

    def test_login_incorrect_passowrd(self, app):
        with raises(expected_exception=IncorrectLoginInformation):
            app.database_connector.create_table("logins", ("username", "password", "email"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.login("test", "Ab1@cdefg")


    def test_login(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email"))
        app.register("test", "Ab1@cdefgh", "gmail.com")
        app.login("test", "Ab1@cdefgh")

    def test_load_user(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email"))
        app.database_connector.add_to_table("logins", ("username", "password", "email", "user"))
        app.load_user()

        assert app.user == "user"

    def test_reload_base(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email"))
        app.register("test", "Ab1@cdefgh", "gmail.com")
        app.reload_base("user")

        assert app.user == "user"

    def test_create_user(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email"))
        app.register("test", "Ab1@cdefgh", "gmail.com")
        app.create_user("a", "b", 10, 10, 10, "male", daily_target=DailyTarget())

        assert app.user.name == "a" and app.user.surname == "b"