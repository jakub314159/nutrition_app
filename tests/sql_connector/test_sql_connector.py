import os
from nutrition_app.sql_connector import SQLConnector


class TestSQLConnector:
    database = "test_database.db"

    def test_01_create_table(self):
        try:
            sql_con = SQLConnector(self.database)
            sql_con.create_table(table_name="users", fields=["id", "name", "surname"])
        except Exception as e:
            raise Exception(e)
        finally:
            os.remove(self.database)

    def test_02_remove_table(self):
        try:
            sql_con = SQLConnector(self.database)
            sql_con.create_table(table_name="users", fields=["id", "name", "surname"])
            sql_con.remove_table(table_name="users")
        except Exception as e:
            raise Exception
        finally:
            os.remove(self.database)

    def test_03_get_existing_tables(self):
        try:
            sql_con = SQLConnector(self.database)
            sql_con.create_table(table_name="users", fields=["id", "name", "surname"])
            tables = sql_con.get_existing_tables()
        except Exception as e:
            tables = None
            pass
        finally:
            os.remove(self.database)

        assert tables == ("users",)

    def test_04_add_to_table_and_get_record(self):
        try:
            sql_con = SQLConnector(self.database)
            sql_con.create_table(table_name="users", fields=("id", "name", "surname"))
            sql_con.add_to_table(table_name="users", records=[(1, "John", "Doe"), (2, "Jane", "Doe")])
            john = sql_con.get_record_from_table(table_name="users", key_name="id", key_val=1)
            jane = sql_con.get_record_from_table(table_name="users", key_name="name", key_val="Jane")
        except Exception as e:
            john = None
            jane = None
        finally:
            os.remove(self.database)

        assert john == {"id": 1, "name": "John", "surname": "Doe"}
        assert jane == {"id": 2, "name": "Jane", "surname": "Doe"}

    def test_05_get_table(self):
        try:
            sql_con = SQLConnector(self.database)
            sql_con.create_table(table_name="users", fields=("id", "name", "surname"))
            sql_con.add_to_table(table_name="users", records=[(1, "John", "Doe"), (2, "Jane", "Doe")])
            table = sql_con.get_table(table_name="users")
        except Exception as e:
            table = {}
        finally:
            os.remove(self.database)

        assert table == {"id": [1, 2], "name": ["John", "Jane"], "surname": ["Doe", "Doe"]}
