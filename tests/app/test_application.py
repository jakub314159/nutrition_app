import json
from pathlib import Path
from pytest import fixture, raises
from base64 import b64encode


from nutrition_app.app.application import (
    App,
    UsernameTakenError,
    EmailTakenError,
    WrongMadePasswordError,
    IncorrectLoginInformation,
)
from nutrition_app.user.daily_target import DailyTarget
from nutrition_app.sql_connector import SQLConnector
from tests.mocked_connector import MockedConnector

LOGIN_DIRPATH = Path(__file__).parent.parent / "test_db" / "test_login_base.json"
USER_DIRPATH = Path(__file__).parent.parent / "test_db" / "test_user_base.json"


LOGIN_SQL_PATH = Path(__file__).parent.parent / "test_db" / "test_nutrition_app_database.db"


@fixture()
def app():
    app = App(database_connector=MockedConnector())
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

    def test_automatic_password(self, app):
        password = app.automatic_password()
        app.check_password(password)

    def test_check_table(self, app):
        val = app._check_table(app._logins_name)
        assert val == True

    def test_delete_table(self, app):
        app._logins_name = "test"
        app.database_connector.create_table("test", (1, 2, 3))
        app._delete_table("test")

        assert app._check_table("test") == False

    def test_create_products_table(self, app):
        app._create_table(app._logins_name, ("1", "2", "3"))
        val = app._check_table(app._logins_name)
        assert val == True

    def test_update_record(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email", "verified"))
        app.register("test", "Ab1@cdefgh", "gmail.com")
        app.database_connector.update_record_in_table("logins", "username", "test", "verified", True)
        app.login("test", "Ab1@cdefgh")
        app._update_record(key_name="password", new_val=1)

        assert (
            app.database_connector.get_record_from_table(table_name="logins", key_name="username", key_val="test")[
                "password"
            ]
            == 1
        )

    def test_save_to_sql_db(self, app):
        app._save_to_logins_db("nie", "tak", "no")
        sql_dict = app.database_connector.get_table("logins")
        assert (
            sql_dict["email"][0] == b64encode("no".encode("utf-8")).decode("utf-8")
            and sql_dict["password"][0] == b64encode("tak".encode("utf-8")).decode("utf-8")
            and sql_dict["username"][0] == "nie"
        )

    def test_register_username_taken_error(self, app):
        with raises(expected_exception=UsernameTakenError):
            app.database_connector.create_table("logins", ("username", "password", "email"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.register("test", "Ab1@cdefgh", "email.com")

    def test_register_email_taken_error(self, app):
        with raises(expected_exception=EmailTakenError):
            app.database_connector.create_table("logins", ("username", "password", "email"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.register("user", "Ab1@cdefgh", "gmail.com")

    def test_register(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email"))
        app.register("test", "Ab1@cdefgh", "gmail.com")

        sql_dict = app.database_connector.get_table("logins")

        assert (
            sql_dict["username"][0] == "test"
            and sql_dict["password"][0] == b64encode("Ab1@cdefgh".encode("utf-8")).decode("utf-8")
            and sql_dict["email"][0] == b64encode("gmail.com".encode("utf-8")).decode("utf-8")
        )

    def test_login_incorrect_username(self, app):
        with raises(expected_exception=IncorrectLoginInformation):
            app.database_connector.create_table("logins", ("username", "password", "email", "verified"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.database_connector.update_record_in_table("logins", "username", "test", "verified", True)
            app.login("test1", "Ab1@cdefgh")

    def test_login_incorrect_password(self, app):
        with raises(expected_exception=IncorrectLoginInformation):
            app.database_connector.create_table("logins", ("username", "password", "email", "verified"))
            app.register("test", "Ab1@cdefgh", "gmail.com")
            app.database_connector.update_record_in_table("logins", "username", "test", "verified", True)
            app.login("test", "Ab1@cdefg")

    def test_login(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email", "verified"))
        app.register("test", "Ab1@cdefgh", "gmail.com")
        app.database_connector.update_record_in_table("logins", "username", "test", "verified", True)
        app.login("test", "Ab1@cdefgh")

        assert app.username == "test"

    def test_create_user(self, app):
        app.database_connector.create_table("logins", ("username", "password", "email", "verified"))
        app.register("test", "Ab1@cdefgh", "gmail.com")
        app.database_connector.update_record_in_table("logins", "username", "test", "verified", True)
        app.create_user("test", "test", 16, 2, 3, "male")
        app.login("test", "Ab1@cdefgh")

        record = app.database_connector.get_record_from_table(app._users_name, "username", "test")
        assert record["name"] == "test" and record["age"] == 16 and record["height"] == 200 and record["weight"] == 3

    def test_create_new_daily_target(self, app):
        app.create_user("test", "test", 16, 2, 3, "male")
        app.create_daily_target(kcal=340, protein=20, fats=20, carbs=20)

        assert app.user.daily_target.kcal == 340

    def test_set_new_daily_target(self, app):
        app.create_user("test", "test", 16, 2, 3, "male")
        app.create_daily_target(activity=3)

        assert app.user.daily_target.kcal == 1550

