import json
import os

from src.utils.json_service import write_to_json


class TestJsonService:
    def setup_method(self):
        self.file_name = "test_data.json"

    def teardown_method(self):
        # Clean up the test data file after each test
        try:
            os.remove(self.file_name)
        except FileNotFoundError:
            pass

    def test_write_to_json_existing_file(self):
        # Arrange
        data = {"name": "John", "age": 30}
        expected_data = [data]

        # Act
        write_to_json(data, self.file_name, print_to_terminal=False)

        # Assert
        with open(self.file_name, "r", encoding="utf-8") as file:
            file_data = json.load(file)
            assert file_data == expected_data

    def test_write_to_json_new_file(self):
        # Arrange
        data = {"name": "Jane", "age": 25}
        expected_data = [data]

        # Act
        write_to_json(data, self.file_name, print_to_terminal=False)

        # Assert
        with open(self.file_name, "r", encoding="utf-8") as file:
            file_data = json.load(file)
            assert file_data == expected_data
