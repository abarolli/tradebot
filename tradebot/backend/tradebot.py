from pprint import pprint
from pathlib import Path

from tradebot.configs import TradebotConfigs
from tradebot.requests import TradebotRequests


class Tradebot:

    def __init__(self, configs:TradebotConfigs, requests:TradebotRequests):
        self.__configs = configs
        self.__tb_requests = requests


    def __request_new_access_token(self, ):

        consumer_key, refresh_token = self.__configs["consumer_key"], self.__configs["refresh_token"]
        auth_url = "https://api.tdameritrade.com/v1/oauth2/token"
        
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": consumer_key + "@AMER.OAUTHAP",
        }

        res = self.__tb_requests.post(auth_url, data=req_body, auth=False)
        if not res.ok:
            raise Exception("Response was not ok; could not get new access token")

        return res.json()


    def update_access_token(self, ):
        new_data = self.__request_new_access_token()
        self.__configs.update(new_data)


    def fundamentals(self, ticker:str):

        url = "https://api.tdameritrade.com/v1/instruments"
        url_params = {"apikey": self.__configs["consumer_key"], "symbol": ticker, "projection": "fundamental"}
        
        res = self.__tb_requests.get(url, params=url_params)
        if not res.ok:
            print("Response was not ok for the url:")
            print("URL: " + url)
            return res

        return res.json()
        

    def quote(self, ticker:str):
        
        url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/quotes"
        res = self.__tb_requests.get(url)
        assert res.ok

        return res.json()


    def price_history(self, ticker:str, period_type:str=None, period:int=None, frequency_type:str=None, frequency:int=None, end_date:int=None, start_date:int=None, need_extended_hours:bool=True):

        url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory"
        api_key = self.__configs["consumer_key"]
        params = {
            "apikey": api_key,
            "periodType": period_type,
            "period": period,
            "frequencyType": frequency_type,
            "frequencey": frequency,
            "endDate": end_date,
            "startDate": start_date,
            "needExtendedHoursData": need_extended_hours
        }

        res = self.__tb_requests.get(url, params=params)
        assert res.ok

        return res.json()