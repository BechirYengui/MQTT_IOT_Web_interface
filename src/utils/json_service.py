"""
This module contains helper functions for reading and writing to json files.
"""

import json


def write_to_json(data, file_name, print_to_terminal=True):
    try:
        with open(file_name, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            if print_to_terminal:
                print(f"Data written to {file_name}: {data}")
    except FileNotFoundError:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump([data], file, indent=4)
            if print_to_terminal:
                print(f"Data written to {file_name}: {data}")


def read_json_file(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
