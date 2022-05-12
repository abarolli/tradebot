from __future__ import annotations
import config.tradebot_config as tradebot_config
from utils.httputils import BadResponseException

import requests
from urllib.parse import urlencode

class TradeBot:

    def __init__(self, configs:tradebot_config.TradeBotConfigs):
        self.__configs = configs
        self.__base_url = "https://api.tdameritrade.com/v1/"

    
    def get_price_history(self, ticket:str, periodType:str, period:int, frequencyType:str, frequency:str):
        apikey = self.__configs.get("consumer_key")
        access_token = self.__configs.get("access_token")
        query_string = urlencode({"apikey": apikey, "periodType": periodType, "period": period, "frequencyType": frequencyType, "frequency": frequency})
        url = f"{self.__base_url}marketdata/{ticket}/pricehistory?{query_string}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        res = requests.get(url, headers=headers)

        if not res.ok:
            raise Exception(f"Got a response of {res.status_code}. Ensure that the provided query parameters are correct and the device is connected to the internet")
        
        return res.json()
        

    def access_token_request(self):
        grant_type = "refresh_token"
        refresh_token = self.__configs.get("refresh_token")
        client_id = self.__configs.get("consumer_key")
        url = f"{self.__base_url}oauth2/token"
        payload = {
            "grant_type": grant_type,
            "refresh_token": refresh_token,
            "client_id": client_id
        }

        res = requests.post(url, data=payload)
        
        if not res.ok:
            raise BadResponseException("Ensure that the provided query parameters are correct and the device is connected to the internet", res)
        
        return res.json()