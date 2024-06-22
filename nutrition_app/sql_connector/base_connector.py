from abc import ABC, abstractmethod

from pathlib import Path
from typing import Sequence, Any



class BaseConnector(ABC):

    @abstractmethod
    def create_table(self, table_name: str, fields: Sequence[str]) -> None:
        """
        Create table in the database with specified name.

        Args:
        table_name(str): name of the table to be created in the database
        fields(Sequence[str]): names of the fields in the table

        Returns:
        None
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_table(self, table_name: str) -> None:
        """
        Remove table from the database.

        Args:
            table_name(str): table to be removed from the database

        Returns:
            None
        """
        raise NotImplementedError()

    @abstractmethod
    def get_existing_tables(self) -> tuple[str, ...]:
        """
        Get names of existing tables in sqlite database.

        Returns:
            tuple[str, ...]: existing tables
                Example: ('users', 'products')
        """
        raise NotImplementedError()

    @abstractmethod
    def add_to_table(self, table_name: str, records: list[tuple]) -> None:
        """
        Add records to the chosen table.

        Args:
            table_name(str): name of the table to which records will be added
            records(list[tuple]): records to be added
                Example: [(field_1_value, field_2_value, ...), ...]

        Returns:
            None
        """
        raise NotImplementedError()

    @abstractmethod
    def get_record_from_table(self, table_name: str, key_name: str, key_val: Any) -> dict[str, Any]:
        """
        Get record from the chosen table with given primary key.
        if the given key won't be primary returned result will be
        the first occurrence satisfying requirement.

        Args:
            table_name(str): name of the table to get records from
            key_name(str): name of the key in the table (e.g. id or username)
            key_val(Any): what value we are looking for

        Returns:
            dict[str, Any]: output data with chosen record as a dict
        """
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        """Close the connection with database."""
        raise NotImplementedError()

    @abstractmethod
    def get_table(self, table_name: str) -> dict[str, Any]:
        """
        Get full table as dict.

        Args:
            table_name(str): name of the table to be returned

        Returns:
            dict[str, list[Any]]: table transformed to a dictionary
        """
        raise NotImplementedError()

    @abstractmethod
    def update_record_in_table(
        self, table_name: str, column_name: str, column_val: Any, update_column: str, new_value: Any
    ) -> None:
        """
        Update a specific value in the chosen table for a given primary key.

        Args:
            table_name(str): name of the table to update records in
            column_name(str): name of the key in the table (e.g. id or username)
            column_val(Any): the key value of the record to update
            update_column(str): the column name of the value to update
            new_value(Any): the new value to be set

        Returns:
            None
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_from_table(self, table_name: str, column_name: str, value: any) -> None:
        """
        Remove records from the chosen table based on the given column and value.

        Args:
            table_name (str): name of the table from which records will be removed
            column_name (str): name of the column to use in the condition
            value (any): value to match for the condition

        Returns:
            None
        """
        raise NotImplementedError()
