from typing import Sequence, TypeAlias, Any

from nutrition_app.sql_connector.base_connector import BaseConnector

TableType: TypeAlias = dict[str, list]

class MockedConnector(BaseConnector):

    def __init__(self, **kwargs):
        self.tables: dict[str, TableType] = {}

    def create_table(self, table_name: str, fields: Sequence[str]) -> None:
        self.tables[table_name] = {x:[] for x in fields}

    def remove_table(self, table_name: str) -> None:
        self.tables.pop(table_name)

    def get_existing_tables(self) -> tuple[str, ...]:
        return tuple([x for x in self.tables.keys()])

    def add_to_table(self, table_name: str, records: list[tuple]) -> None:
        for record in records:
            for record_name, record_value in zip(self.tables[table_name], record):
                self.tables[table_name][record_name].append(record_value)

    def get_record_from_table(self, table_name: str, key_name: str, key_val: Any) -> dict[str, Any]:
        v = [dict(zip(self.tables[table_name], t)) for t in zip(*self.tables[table_name].values())]
        for e in v:
            if e[key_name] == key_val:
                return e
        raise ValueError("key_val not found")

    def get_table(self, table_name: str) -> dict[str, Any]:
        return self.tables[table_name]

    def update_record_in_table(
    self, table_name: str, primary_key_name: str, primary_key_val: Any, key_name: str, new_value: Any
) -> None:
        index = self.tables[table_name][primary_key_name].index(primary_key_val)
        self.tables[table_name][key_name][index] = new_value

    def remove_from_table(self, table_name: str, column_name: str, value: any) -> None:
        pass