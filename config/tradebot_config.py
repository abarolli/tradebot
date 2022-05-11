from __future__ import annotations
import os

from utils import fileutils
from utils.utils import singleton, check_singleton

__this_dir = os.path.dirname(__file__)
settings_file = fileutils.join(__this_dir, "settings.yml")


@singleton
class TradeBotConfigs:

    @staticmethod
    def get_config() -> TradeBotConfigs:
        if TradeBotConfigs.__instance:
            return TradeBotConfigs.__instance
        else:
            self = TradeBotConfigs()
            self.__data = fileutils.read(settings_file, fileutils.yml_to_dict)
            TradeBotConfigs.__instance = self
            return self


    @check_singleton
    def get(self, key:str) -> str:
        return self.__data.get(key)


    @check_singleton
    def update(self, key:str, value:str) -> None:
        entry = {key:value}
        self.__data.update(entry)