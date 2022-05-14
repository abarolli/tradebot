from __future__ import annotations
import os
from typing import Mapping

from utils import fileutils
from utils.utils import singleton, check_singleton
import bot.tradebot as tradebot


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
    def update(self, new_data:Mapping[str, str]) -> None:
        self.__data.update(new_data)


    @check_singleton
    def write_new_access_token(self, bot:tradebot.TradeBot):
        new_data = bot.post_access_token()
        self.update(new_data) #update self.__data
        fileutils.update_yml(settings_file, self.__data)