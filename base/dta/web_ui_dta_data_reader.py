import configparser
from pojo.dta.web_ui_dta_config import WebUIDtaConfig
from common.data_reader_tool import DataReaderTool


class WebUIDtaDataReader(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.data = self._read_data('test_data/web_ui/dta/web_ui_dta_data.json')
            self.__inited = True

    def _read_data(self, config_file):
        return DataReaderTool.load_json(config_file)
