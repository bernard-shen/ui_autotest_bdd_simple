import json
from configparser import ConfigParser


class DataReaderTool:
    @classmethod
    def load_json(cls, file_path):
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        return data
