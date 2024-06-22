from nutrition_app.sql_connector import SQLConnector

class TestSQLConnector:

    def test_01_create_table(self, tmp_path):
        sql_con = SQLConnector(tmp_path / "database.db")
        sql_con.create_table(table_name="users", fields=["id", "name", "surname"])



    def test_02_remove_table(self, tmp_path):
        sql_con = SQLConnector(tmp_path / "database.db")
        sql_con.create_table(table_name="users", fields=["id", "name", "surname"])
        sql_con.remove_table(table_name="users")
        assert sql_con.get_existing_tables() is None


    def test_03_get_existing_tables(self, tmp_path):
        sql_con = SQLConnector(tmp_path / "database.db")
        sql_con.create_table(table_name="users", fields=["id", "name", "surname"])
        tables = sql_con.get_existing_tables()

        assert tables == ("users",)

    def test_04_add_to_table_and_get_record(self, tmp_path):

        sql_con = SQLConnector(tmp_path / "database.db")
        sql_con.create_table(table_name="users", fields=("id", "name", "surname"))
        sql_con.add_to_table(table_name="users", records=[(1, "John", "Doe"), (2, "Jane", "Doe")])
        john = sql_con.get_record_from_table(table_name="users", key_name="id", key_val=1)
        jane = sql_con.get_record_from_table(table_name="users", key_name="name", key_val="Jane")

        assert john == {"id": 1, "name": "John", "surname": "Doe"}
        assert jane == {"id": 2, "name": "Jane", "surname": "Doe"}

    def test_05_get_table(self, tmp_path):
        sql_con = SQLConnector(tmp_path / "database.db")
        sql_con.create_table(table_name="users", fields=("id", "name", "surname"))
        sql_con.add_to_table(table_name="users", records=[(1, "John", "Doe"), (2, "Jane", "Doe")])
        table = sql_con.get_table(table_name="users")

        assert table == {"id": [1, 2], "name": ["John", "Jane"], "surname": ["Doe", "Doe"]}

    def test_06_update_record_in_table(self, tmp_path):
        sql_con = SQLConnector(tmp_path / "database.db")
        sql_con.create_table(table_name="users", fields=("id", "name", "surname"))
        sql_con.add_to_table(table_name="users", records=[(1, "John", "Doe")])
        old_val = sql_con.get_record_from_table("users", key_name="id", key_val=1)["name"]
        sql_con.update_record_in_table(table_name="users", primary_key_name="id", primary_key_val=1, key_name="name", new_value="a")
        assert sql_con.get_record_from_table("users", key_name="id", key_val=1)["name"] != old_val

    def test_07_remove_from_table(self, tmp_path):
        sql_con = SQLConnector(tmp_path / "database.db")
        sql_con.create_table(table_name="users", fields=("id", "name", "surname"))
        sql_con.add_to_table(table_name="users", records=[(1, "John", "Doe"), (2, "Jane", "Doe")])
        old_val = sql_con.get_table("users")["name"]
        sql_con.remove_from_table("users", "id", 1)

        assert sql_con.get_table("users")["name"] != old_val