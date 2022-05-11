from config.tradebot_config import TradeBotConfigs

import requests
from urllib.parse import urlencode

from pprint import pprint


class TradeBot:

    def __init__(self, configs:TradeBotConfigs):
        self.__configs = configs
        self.__base_url = "https://api.tdameritrade.com/v1/"

    
    def get_price_history(self, ticket:str, periodType:str, period:int, frequencyType:str, frequency:str):
        apikey = self.__configs.get("consumer_key")
        access_token = self.__configs.get("access_token")
        query_string = urlencode({"apikey": apikey, "periodType": periodType, "period": period, "frequencyType": frequencyType, "frequency": frequency})
        url = self.__base_url + f"marketdata/{ticket}/pricehistory?" + query_string
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        res = requests.get(url, headers=headers)
        data = res.json()

        return data