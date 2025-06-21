import configparser
from pojo.web_ui_config import WebUIConfig


class WebUIConfReader(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config = self._read_config('config/web_ui.conf')
            self.__inited = True

    def _read_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        web_ui_config = WebUIConfig()
        web_ui_config.test_workers = config.get('test', 'test_workers')
        web_ui_config.test_browsers = config.get('browser', 'test_browsers').split('||')
        web_ui_config.current_browser = config.get('browser', 'current_browser')
        web_ui_config.download_dir = config.get('browser', 'download_dir')
        web_ui_config.is_headed = config.get('browser', 'is_headed')
        return web_ui_config
