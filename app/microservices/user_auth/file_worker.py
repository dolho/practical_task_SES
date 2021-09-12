import os
import json
import pathlib


class FileWorker:

    def __init__(self, directory_of_user_data = os.path.join(pathlib.Path(__file__).parent.absolute(), "user_data")):
        self.__directory_of_user_data = directory_of_user_data

    def get_path_to_file(self, name_of_file, format_of_file=".json"):
        return os.path.join(self.__directory_of_user_data, name_of_file + format_of_file)

    def read_file(self, path_to_file):
        is_file_already_exists = os.path.isfile(path_to_file)
        if not is_file_already_exists:
            raise FileNotFoundError
        with open(path_to_file, 'r') as f:
            data = json.load(f)
            return data

    def append_to_file(self, path_to_file, info: dict):
        is_file_already_exists = os.path.isfile(path_to_file)
        if is_file_already_exists:
            with open(path_to_file, 'r+') as f:
                data = json.load(f)
                data.append(info)
                FileWorker.overwrite_file(f, data)
        else:
            raise FileNotFoundError

    def create_file(self, path_to_file, info: list):
        with open(path_to_file, 'w') as f:
            json.dump(info, f)


    @staticmethod
    def overwrite_file(file, data):
        file.seek(0)
        file.truncate()
        json.dump(data, file)

    @staticmethod
    def overwrite_file_by_path(path_to_file, data):
        with open(path_to_file, 'w') as file:
            file.seek(0)
            file.truncate()
            json.dump(data, file)