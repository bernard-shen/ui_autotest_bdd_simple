import configparser
from pojo.dta.web_ui_dta_config import WebUIDtaConfig


class WebUIDtaConfReader(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config = self._read_config('config/dta/web_ui_dta.conf')
            self.__inited = True

    def _read_config(self, config_file):
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read(config_file, encoding='utf-8')
        web_ui_dta_config = WebUIDtaConfig()
        web_ui_dta_config.host = config.get('server', 'host')
        web_ui_dta_config.pages = dict(config.items('pages'))
        return web_ui_dta_config

